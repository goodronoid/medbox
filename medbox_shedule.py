#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import urllib
import re
import sys

prms = {
	"city" : "Нижневартовск",
	"alias" : "NVRD",
	"dept" : "4",
	"name" : "Детская поликлиника №1",
	"lid" : "100"
	}
s = requests.session()

r = s.get("https://medbox.ru/2016/Schedule", params = prms)

r = s.post('https://medbox.ru/2016/Schedule/LpuSearch', data={"CityName" : "Нижневартовск"})
r = s.post("https://medbox.ru/2016/Schedule/SpecSearch", data={"connAlias": "NVRD", "s_lpu": "4", "lid": "100"})
r = s.post("https://medbox.ru/2016/Schedule/DocSearch", data={"connAlias": "NVRD", "depNum": "4", "spec": "-999"})

schedule = eval(str(bs(r.content, 'lxml').text))
medspec_list = set()
for s in schedule:
    medspec_list.add(s['medspec'])
medspec_list = tuple(sorted(medspec_list))

print("\nВыберите специальность :")
for n, s in enumerate(medspec_list, 1):
    print(n, '->', s)

medspec_choosen = medspec_list[int(input())-1]

doctors_list = []
for s in schedule:
	if s['medspec'] == medspec_choosen and s['freetime'] > 0:
		doctors_list.append(s)
		print(s['medspec'], s['name'], "\nСвободных мест:", s['freetime'], '\n')

if len(doctors_list) == 0:
	print("\nСвободных мест нет!\n")
    ### ЗАПУСК ДЕМОНА АВТОЗАПИСИ

input('КОНЕЦ')
# # просто сохраним страницу в html-файл:
# soup = bs(r.content, 'html.parser')
# with open('medbox0_SHEDULE.html', 'w', encoding='utf-8') as output_file:
#     output_file.write(soup.prettify())
