# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
# from lxml import html
# import urllib
import re, sys

session = requests.Session()
session.headers.update({
    # 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding' : 'gzip,deflate,sdch',
    # 'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
})

# 1 https://medbox.ru/2016/
r = session.get('https://medbox.ru/2016/')

# session_id = r.headers['Set-Cookie'][18:42]

sys.stdout.write("\033[0;33m")  # orange
# print('\n' + bs(r.content, 'lxml').findAll('h3')[1].text + ':\n')
print("Выберите город и регион:\n \nРегион:")

print("00 -> Список всех городов")
for x in bs(r.content, 'lxml').find('select', attrs={'id': 'region_selector'}).findAll('option'):
    print(x['value'], "->", x.text)

sys.stdout.write("\033[0;32m")  # green
user_region = input()
sys.stdout.write("\033[0;33m")  # orange

print('\nГоргород:')
city_list = dict()

# need REFACTORING (copy-pasting)
if user_region == '86': # Первый в списке ХМАО
    for x, xx in enumerate(bs(r.content, 'lxml').findAll('select')[1].findAll('option'), 1):
        print(x, '->', xx.text)
        city_list[x] = xx.text
elif user_region == '89': # Второй в списке ЯНАО
    for x, xx in enumerate(bs(r.content, 'lxml').findAll('select')[2].findAll('option'), 1):
        print(x, '->', xx.text)
        city_list[x] = xx.text
elif user_region == '72': # Третий в списке Тмн
    for x, xx in enumerate(bs(r.content, 'lxml').findAll('select')[3].findAll('option'), 1):
        print(x, '->', xx.text)
        city_list[x] = xx.text
elif user_region == '00':
    lst = []
    for i in range(1, 4):
        for xx in bs(r.content, 'lxml').findAll('select')[i].findAll('option'):
            lst.append(xx.text)
    for x, xx in enumerate(sorted(lst), 1):
        print(x, '->', xx)
        city_list[x] = xx
else:
    raise Exception('Надо выбрать один из предложенных вариантов. Попробуйте ещё раз.')  # FIX FIX FIX


sys.stdout.write("\033[0;32m")  # green
city = city_list[int(input())]
sys.stdout.write("\033[0;33m")  # orange

# 2 'https://medbox.ru/2016/Rec/SelectDept'
r = session.post(
    url=r.url,
    data={'nextButton': 'Продолжить', 'citylist': city},
    headers={'Referer': r.url})

hospital_list = dict()
print(bs(r.content, 'lxml').findAll('h3')[1].text, ':')  # Выберите лечебное учреждение:
for x, xx in enumerate(bs(r.content, 'lxml').findAll('select')[0].findAll('option'), 1):
    hospital_list[x] = [xx.text, xx['value']]
    print(x, '->', xx.text)

sys.stdout.write("\033[0;32m")  # green
hospital = hospital_list[int(input())][1]
sys.stdout.write("\033[0;33m")  # orange

# 3 https://medbox.ru/2016/Rec/Identification
r = session.post(
    url=r.url,
    data={'nextButton': 'Продолжить', 'departments': hospital},
    headers={'Referer': r.url}
)
print('\n')

std_in = sys.stdin
f = open('../personal_data')
sys.stdin = f
SecondName = input("Введите Фамилию:\n")
FirstName = input("Введите Имя:\n")
MiddleName = input("Введите Отчество:\n")
DateOfBirth = input("Дата рождения (в формате ДД.ММ.ГГГГ):\n")
PolicySerNum = input("№ медицинского полиса:\n")
PhoneNumber = input("Номер телефона (в формате +7 (ХХХ) ХХХ-ХХ-ХХ):\n")
sendSMS = input("Получать СМС-уведомления (true/false):\n")
sys.stdin = std_in

# 4 'https://medbox.ru/2016/Rec/CurrentRecords'
r = session.post(
    url=r.url,
    data={
        'person.SecondName': SecondName,
        'person.FirstName': FirstName,
        'person.MiddleName': MiddleName,
        'person.DateOfBirth': DateOfBirth,
        'person.PolicySerNum': PolicySerNum,
        'person.PhoneNumber': PhoneNumber,
        'person.sendSMS': sendSMS,
        # 'person.sendSMS' : 'false',
        'person.SaveData': 'true',
        # 'person.SaveData' : 'false',
        'person.Agreement': 'true',
        # 'person.Agreement' : 'false',
        'nextButton': 'Продолжить'
        # 'nextButton': ''
    },
    headers={'Referer': r.url}
)

# Error:
# Сервис идентификации ТФОМС недоступен. Попробуйте повторить попытку позднее.
# html.body.div.div.div.div.div.div. span.field-validator-error
# <span class="field-validation-error">Сервис идентификации ТФОМС недоступен.
# Попробуйте повторить попытку позднее.</span>

# print('r:\n URL:', r.url, r.history, '\n', 'Status:', r, '\n', 'Cookies:', r.cookies.get_dict(), session.cookies.get_dict(), '\n')

# 4b 'https://medbox.ru/2016/Rec/CurrentRecords'
if r.url == 'https://medbox.ru/2016/Rec/CheckMissedAppts':
    errtext = bs(r.content, 'lxml').find(style='color:Red')
    sys.stdout.write("\033[0;31m")  # red
    print(' '.join(errtext.text.split()))
    print('\n'.join(re.split('\n{1,} *', errtext.nextSibling.nextSibling.text)))
    sys.stdout.write("\033[0;33m")  # orange
    r = session.post(url=r.url, data={'nextButton': 'Продолжить'})

xx = bs(r.content, 'lxml').find(name='div', attrs={'class': 'visit visit--old'})
print("Ваши текущие приёмы:\n", re.search('([А-Яа-ё+]+ *)+', xx.text).group(0))

# 5 'https://medbox.ru/2016/Rec/SelectSpec'
r = session.post(url=r.url, data={'nextButton': 'Продолжить'})
xx = bs(r.content, 'lxml').find(name='select', attrs={"class": "select2-offscreen"})

# # просто сохраним страницу в html-файл:
# soup = bs(r.content, 'html.parser')
# with open('medbox4_CheckMissedAppts.html', 'w', encoding='utf-8') as output_file:
#     output_file.write(soup.prettify())


sys.stdout.write("\033[0;32m")  # green
input("КОНЕЦ")
