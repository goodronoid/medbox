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
print('r:\n URL:', r.url, r.history, '\n', 'Status:', r, '\n', 'Cookies:', r.cookies.get_dict(), s.cookies.get_dict(), '\n')

session_id = r.headers['Set-Cookie'][18:42]
data = {}
data['nextButton'] = 'Продолжить'
data['citylist'] = 'Нижневартовск'

r2 = s.post(url=medurl, data=data, headers = {'Referer': r.url})
print('r2:\n URL:', r2.url, r2.history, '\n', 'Status:', r2, '\n', 'Cookies:', r2.cookies.get_dict(), s.cookies.get_dict(), '\n')
