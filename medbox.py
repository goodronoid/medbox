#-*-coding:utf8;-*-

import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import urllib

medurl = 'https://medbox.ru/2016/'

# standart headers
headers_standart = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
           'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding' : 'gzip,deflate,sdch',
           'Accept-Language' : 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
           'Cache-Control' : 'max-age=0'}

# headers from Chrome
headers_chrome = {
	'Set-Cookie': 'ASP.NET_SessionId=3m2ffcykz4cb1om523vr4jtp; _ym_uid=1509363136916671318; __Region=%7B%22Region%22%3A%2286%22%2C%22Name%22%3A%22%D0%9D%D0%B8%D0%B6%D0%BD%D0%B5%D0%B2%D0%B0%D1%80%D1%82%D0%BE%D0%B2%D1%81%D0%BA%22%7D; _ga=GA1.2.1083857719.1509363136'
}

cookies_chrome = {
	'_ga' : 'GA1.2.1083857719.1509363136',
	'_ym_uid' : '1509363136916671318',
	'__Region' : '%7B%22Region%22%3A%2286%22%2C%22Name%22%3A%22%D0%9D%D0%B8%D0%B6%D0%BD%D0%B5%D0%B2%D0%B0%D1%80%D1%82%D0%BE%D0%B2%D1%81%D0%BA%22%7D'
}

# headers_2 = {'Cookie' : 'IdentData=FirstName=%d0%a1%d0%be%d1%84%d0%b8%d1%8f&SecondName=%d0%90%d0%bb%d0%b5%d0%ba%d1%81%d0%b5%d0%b5%d0%bd%d0%ba%d0%be-%d0%9d%d0%b5%d0%b4%d1%8b%d1%88%d0%b8%d0%bb%d0%be%d0%b2%d0%b0&MiddleName=%d0%90%d0%bd%d0%b4%d1%80%d0%b5%d0%b5%d0%b2%d0%bd%d0%b0&YearOfBirth=1983&DateOfBirth=05.03.2007+0%3a00%3a00&PolicySerNum=8196299794000757&Snils=&PhoneNumber=79227914474&Kindcost=1; __Region=%7B%22Region%22%3A%2286%22%2C%22Name%22%3A%22%D0%9D%D0%B8%D0%B6%D0%BD%D0%B5%D0%B2%D0%B0%D1%80%D1%82%D0%BE%D0%B2%D1%81%D0%BA%22%7D',
#            'Referer': 'https://medbox.ru/2016/'}

# post method
# data = {'citylist' : '%D0%9D%D0%B8%D0%B6%D0%BD%D0%B5%D0%B2%D0%B0%D1%80%D1%82%D0%BE%D0%B2%D1%81%D0%BA', 
#     'nextButton' : '%D0%9F%D1%80%D0%BE%D0%B4%D0%BE%D0%BB%D0%B6%D0%B8%D1%82%D1%8C'}

data = {}
data['nextButton'] = urllib.parse.quote('Продолжить')
data['citylist'] = urllib.parse.quote('Нижневартовск')

s = requests.Session()
s.headers.update(headers_standart) # может это лишнее ?
r = s.get(medurl)
print(r.url, r.history)
print('Status:', r)
print('Cookies:', r.cookies.get_dict())


d = str(r.headers['Set-Cookie']).split('; ')

requests.cookies.remove_cookie_by_name(s.cookies, '__Region')
requests.cookies.merge_cookies(s.cookies, cookies_chrome)

r.headers['Set-Cookie'] = 'ASP.NET_SessionId=sogtxqjljuyfg25xaq5nlbc3; path=/; HttpOnly, __Region=%7B%22Region%22%3A%2286%22%2C%22Name%22%3A%22%D0%9D%D0%B8%D0%B6%D0%BD%D0%B5%D0%B2%D0%B0%D1%80%D1%82%D0%BE%D0%B2%D1%81%D0%BA%22%7D; path=/; _ym_uid=1509363136916671318; path=/; _ga=GA1.2.1083857719.1509363136; path=/'
# 'ASP.NET_SessionId=wof2vqi0u1az03qslwkx1rdk; path=/; HttpOnly, __Region={"End":3000518655,"Region":"86","Name":"Ð\x9dÐ¸Ð¶Ð½ÐµÐ²Ð°Ñ\x80Ñ\x82Ð¾Ð²Ñ\x81Ðº"}; path=/'

# # просто сохраним страницу в html-файл:
# soup = bs(r.content, 'html.parser')
# with open('medbox.html', 'w', encoding='utf-8') as output_file:
#     output_file.write(soup.prettify())
#
# # 
# region = soup.find('select', id = 'region_selector')
# print(region.prettify())
# city = soup.find('span', id = 'hmao_town_list')
# nv86 = city.find('option', value = 'Нижневартовск')
# print(nv86)

s.headers.update(r.headers) # может это лишнее ?
r2 = s.post(url=medurl, data=data, headers = {'Referer': medurl})

#r2 = s.post(url=medurl, data=data, cookies = s.cookies, headers = s.headers)
print('URL:', r2.url, r2.history)
print('Status:', r2)
print('Cookies:', r2.cookies)

r3 = s.get('https://medbox.ru/2016/Rec/SelectDept', headers = {'Referer': r2.url})
print(r3.url, r3.history)
print('Status:', r3)
print('Cookies:', r3.cookies)
