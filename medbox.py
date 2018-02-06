# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
# from lxml import html
# import urllib
import re, sys
import medbox_schedule, medbox_requests

personal_data_dict = medbox_requests.personal_data()

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
})

# 1 https://medbox.ru/2016/
r = session.get('https://medbox.ru/2016/')

# session_id = r.headers['Set-Cookie'][18:42]

city = medbox_requests.choose_your_city(r)

steps_dict = {
    'https://medbox.ru/2016/': {
        'next_url': 'https://medbox.ru/2016/Rec/SelectDept',
        'data': {'citylist': city}
    },
    'https://medbox.ru/2016/Rec/SelectDept': {
        'next_url': 'https://medbox.ru/2016/Rec/Identification',
        'data': {}
    },
    'https://medbox.ru/2016/Rec/Identification': {
        'next_url': 'https://medbox.ru/2016/Rec/CurrentRecords',
        'data': personal_data_dict
    },
    'https://medbox.ru/2016/Rec/CheckMissedAppts': {
        'next_url': 'https://medbox.ru/2016/Rec/CurrentRecords',
        'data': {}
    },
    'https://medbox.ru/2016/Rec/CurrentRecords': {

    }
}

# 2 'https://medbox.ru/2016/Rec/SelectDept'
session, r = medbox_requests.rqst(session, r, steps_dict[r.url]['data'])

hospital_list = dict()
print("\n", bs(r.content, 'lxml').findAll('h3')[1].text, ':')  # Выберите лечебное учреждение:
for x, xx in enumerate(bs(r.content, 'lxml').findAll('select')[0].findAll('option'), 1):
    hospital_list[x] = [xx.text, xx['value']]
    print(x, '->', xx.text)

sys.stdout.write("\033[0;32m")  # green
x = hospital_list[int(input())]
hospital = dict()
hospital["name"] = x[0]
hospital["alias"], hospital["lid"], hospital["dept"], hospital["XYN"] = x[1].split(";")
sys.stdout.write("\033[0;33m")  # orange

# 3 https://medbox.ru/2016/Rec/Identification
session, r = medbox_requests.rqst(session, r, {'nextButton': 'Продолжить', 'departments': ";".join((hospital["alias"], hospital["lid"], hospital["dept"], hospital["XYN"]))})

# print('\n')

# 4 'https://medbox.ru/2016/Rec/CurrentRecords'
session, r = medbox_requests.rqst(session, r, steps_dict[r.url]['data'])

# Error:
# Сервис идентификации ТФОМС недоступен. Попробуйте повторить попытку позднее.
# html.body.div.div.div.div.div.div. span.field-validator-error
# <span class="field-validation-error">Сервис идентификации ТФОМС недоступен.
# Попробуйте повторить попытку позднее.</span>

# print('r:\n URL:', r.url, r.history, '\n', 'Status:', r, '\n', 'Cookies:', r.cookies.get_dict(), session.cookies.get_dict(), '\n')

if r.url == 'https://medbox.ru/2016/Rec/CheckMissedAppts':
    errtext = bs(r.content, 'lxml').find(style='color:Red')
    sys.stdout.write("\033[0;31m")  # red
    print()
    problem_error_text = ' '.join(errtext.text.split()) ######################## FIX IT Каждое предолжение с новой строки
    print(problem_error_text)
    print('\n'.join(re.split('\n{1,} *', errtext.nextSibling.nextSibling.text)))
    sys.stdout.write("\033[0;33m")  # orange

# 4b 'https://medbox.ru/2016/Rec/CurrentRecords'
    session, r = medbox_requests.rqst(session, r, steps_dict[r.url]['data'])

xx = bs(r.content, 'lxml').find(name='div', attrs={'class': 'visit visit--old'})
problem_error_text = re.search('([А-Яа-ё+]+ *)+', xx.text).group(0) ############### FIX IT Не работает если список != 1
print("Ваши текущие приёмы:\n", problem_error_text)

# 5 'https://medbox.ru/2016/Rec/SelectSpec'
r = session.post(url=r.url, data={'nextButton': 'Продолжить'})
xx = bs(r.content, 'lxml').find(name='select', attrs={"class": "select2-offscreen"})

# FIX FIX FIX
# ВЗЯТЬ СПИСОК ВРАЧЕЙ СО СТРАНИЦЫ /SelectSpec, а не /Schedule/DocSearch модуля medbox_schedule

# # просто сохраним страницу в html-файл:
# soup = bs(r.content, 'html.parser')
# with open('medbox4_CheckMissedAppts.html', 'w', encoding='utf-8') as output_file:
#     output_file.write(soup.prettify())

doctors_list, medspec = medbox_schedule.get_schedule(city=city, alias=hospital["alias"], dept=hospital["dept"], name=hospital["name"], lid=hospital["lid"])

if len(doctors_list) == 0:
    print("\nСвободных мест нет!\n")
    # ЗАПУСК ДЕМОНА АВТОЗАПИСИ

# 6 https://medbox.ru/2016/Rec/SelectTime
# Аргирова Мария Константиновна
r = session.post(url=r.url, data={"doctor.medspecid": "-999", "doctor.doctorComplexId": "472;2", "infoChecked": "false", "nextButton": "Продолжить"})

# 7 https://medbox.ru/2016/Rec/Complete
# Вы хотите записаться на прием 31 января 2018 18:50, каб. 10.
# Ваш врач — Аргирова Мария Константиновна, педиатр участковый, Детская поликлиника №2, г. Нижневартовск.
r = session.post(url=r.url, data={"id_zapis": "9713067", "nextbutton": "Записаться"})

sys.stdout.write("\033[0;32m")  # green
input("КОНЕЦ medbox")
