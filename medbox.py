#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import urllib
import re, sys

s = requests.Session()
s.headers.update({
    # 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding' : 'gzip,deflate,sdch',
    # 'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
	'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
	})
	
r = s.get('https://medbox.ru/2016/')

# session_id = r.headers['Set-Cookie'][18:42]

sys.stdout.write("\033[0;33m") # orange
# print(bs(r.content, 'lxml').h1.text) # Запись на приём
print(bs(r.content, 'lxml').findAll('h3')[1].text, ':') # Выберите город и регион:

print('Регион:')
regions = dict()
# for x, xx in enumerate(bs(r.content, 'lxml').find('select', attrs={'id' : 'region_selector'}).findAll('option'), 1):
# 	print(x, '->', xx.text)
# 	regions[x] = xx.text

for x in bs(r.content, 'lxml').find('select', attrs={'id' : 'region_selector'}).findAll('option'):
	print("00 -> Список всех городов")
	print(x['value'], "->", x.text)
	regions['0'] = "Список всех городов"
	regions[x['value']] = x.text

####### CHEKKKK #####

regions[x+1] = 'Показать полный список всех городов'
print(x+1, '->', regions[x+1])
sys.stdout.write("\033[0;32m") # green
user_region = int(input())
sys.stdout.write("\033[0;33m") # orange

print('Горгород:')
citylist = dict()
if 0 < user_region < len(regions):
	for x, xx in enumerate(bs(r.content, 'lxml').findAll('select')[user_region].findAll('option'), 1):
		print(x, '->', xx.text)
		citylist[x] = xx.text
elif user_region == len(regions):
	lst = []
	for i in range(1, len(regions)):
		for xx in bs(r.content, 'lxml').findAll('select')[i].findAll('option'):
			lst.append(xx.text)
	for x, xx in enumerate(sorted(lst), 1):
		print(x, '->', xx)
		citylist[x] = xx
else:
	print('Надо выбрать один из предложенных вариантов. Попробуйте ещё раз.') # FIX FIX FIX

sys.stdout.write("\033[0;32m") # green
r = s.post(
	url=r.url, 
	data={'nextButton' : 'Продолжить', 'citylist' : citylist[int(input())]}, 
	headers = {'Referer': r.url})
sys.stdout.write("\033[0;33m") # orange

hospitals = dict()
# print(bs(r.content, 'lxml').h1.text) # Запись на приём
print(bs(r.content, 'lxml').findAll('h3')[1].text, ':') # Выберите лечебное учреждение:
for x, xx in enumerate(bs(r.content, 'lxml').findAll('select')[0].findAll('option'), 1):
	hospitals[x] = [xx.text, xx['value']]
	print(x, '->', xx.text)

sys.stdout.write("\033[0;32m") # green
r = s.post(
	url=r.url, 
	data={'nextButton' : 'Продолжить', 'departments' : hospitals[int(input())][1]},
	headers={'Referer': r.url}
	)
print('\n')


stdin = sys.stdin
f = open('../personal_data')
sys.stdin = f
SecondName = input("Введите Фамилию:\n")
FirstName = input("Введите Имя:\n")
MiddleName = input("Введите Отчество:\n")
DateOfBirth = input("Дата рождения (в формате ДД.ММ.ГГГГ):\n")
PolicySerNum = input("№ медицинского полиса:\n")
PhoneNumber = input("Номер телефона (в формате +7 (ХХХ) ХХХ-ХХ-ХХ):\n")
sendSMS = input("Получать СМС-уведомления (true/false):\n")

r = s.post(
	url=r.url,
	data={
	'person.SecondName' : SecondName, 
	'person.FirstName' : FirstName,
	'person.MiddleName' : MiddleName,
	'person.DateOfBirth' : DateOfBirth,
	'person.PolicySerNum' : PolicySerNum,
	'person.PhoneNumber' : PhoneNumber,
	'person.sendSMS' : sendSMS,
	# 'person.sendSMS' : 'false',
	'person.SaveData' : 'true',
	# 'person.SaveData' : 'false',
	'person.Agreement' : 'true',
	# 'person.Agreement' : 'false',
	'nextButton' : 'Продолжить',
	'nextButton' : ''
	},
	headers={'Referer': r.url}
	)

sys.stdin = stdin


# Error:
# Сервис идентификации ТФОМС недоступен. Попробуйте повторить попытку позднее.
# html.body.div.div.div.div.div.div. span.field-validator-error
# <span class="field-validation-error">Сервис идентификации ТФОМС недоступен.
# Попробуйте повторить попытку позднее.</span>

# print('r:\n URL:', r.url, r.history, '\n', 'Status:', r, '\n', 'Cookies:', r.cookies.get_dict(), s.cookies.get_dict(), '\n')


if r.url == 'https://medbox.ru/2016/Rec/CheckMissedAppts':
	errtext = bs(r.content, 'lxml').find(style='color:Red')
	sys.stdout.write("\033[0;31m") # red
	print(' '.join(errtext.text.split()))
	print('\n'.join(re.split('\n{1,} *', errtext.nextSibling.nextSibling.text)))
	sys.stdout.write("\033[0;33m") # orange
	r = s.post(url=r.url, data={'nextButton' : 'Продолжить'})

xx = bs(r.content, 'lxml').find(name='div', attrs={'class' : 'visit visit--old'})
print("Ваши текущие приёмы:\n", re.search('([А-Яа-ё+]+ *)+', xx.text).group(0))

r = s.post(url=r.url, data={'nextButton' : 'Продолжить'})
xx = bs(r.content, 'lxml').find(name='select', attrs={"class" : "select2-offscreen"})



# # просто сохраним страницу в html-файл:
# soup = bs(r.content, 'html.parser')
# with open('medbox4_CheckMissedAppts.html', 'w', encoding='utf-8') as output_file:
#     output_file.write(soup.prettify())


sys.stdout.write("\033[0;32m") # green