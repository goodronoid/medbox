# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import urllib
import re, sys
import medbox_schedule


def choose_your_city(r):
    sys.stdout.write("\033[0;33m")  # orange
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
    global city
    city = city_list[int(input())]
    sys.stdout.write("\033[0;33m")  # orange

    return user_region, city


def rqst(s, r, data):
    r = s.post(
        url=r.url,
        data=data,
        headers={'Referer': r.url}
    )

    return s, r
