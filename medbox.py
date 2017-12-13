#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import urllib

medurl = 'https://medbox.ru/2016/'

# standart headers
headers_standart = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
           'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding' : 'gzip,deflate,sdch',
           'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'
           }

s = requests.Session()
s.headers.update(headers_standart)

r = s.get(medurl)
# print('r:\n URL:', r.url, r.history, '\n', 'Status:', r, '\n', 'Cookies:', r.cookies.get_dict(), s.cookies.get_dict(), '\n')

session_id = r.headers['Set-Cookie'][18:42]


# soup = bs(r.content, 'lxml')
print(bs(r.content, 'lxml').h1.text) # Запись на приём
print(bs(r.content, 'lxml').findAll('h3')[1].text, ':') # Выберите город и регион:

print('Регион:')
regions = dict()
for x, xx in enumerate(bs(r.content, 'lxml').findAll('select')[0].findAll('option'), 1):
	print(x, '->', xx.text)
	regions[x] = xx.text
regions[x+1] = 'Показать полный список всех городов'
print(x+1, '->', regions[x+1])

user_region = int(input())

print('Город:')
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
del(user_region, lst, x, xx)

# data = {}
# data['nextButton'] = 'Продолжить'
# data['citylist'] = citylist[int(input())]

r2 = s.post(url=medurl, data={'nextButton' : 'Продолжить', 'citylist' : citylist[int(input())]}, headers = {'Referer': r.url})
# print('r2:\n URL:', r2.url, r2.history, '\n', 'Status:', r2, '\n', 'Cookies:', r2.cookies.get_dict(), s.cookies.get_dict(), '\n')

hospitals = dict()
print(bs(r2.content, 'lxml').h1.text) # Запись на приём
print(bs(r2.content, 'lxml').findAll('h3')[1].text, ':') # Выберите лечебное учреждение:
for x, xx in enumerate(bs(r2.content, 'lxml').findAll('select')[0].findAll('option'), 1):
	print(x, '->', xx.text)
	hospitals[x] = xx.text

