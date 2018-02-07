#-*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
from lxml import html
import urllib
import re
import sys


def get_schedule(city="Нижневартовск", alias=0, dept=0, name=0, lid=0):
    session = requests.session()
    prms = {
        "city": city,
        "alias": alias,
        "dept": dept,
        "name": name,
        "lid": lid
    }

    if not (alias and name and dept and lid):
        print("не указан ни один из параметров")
        return

    r = session.get("https://medbox.ru/2016/Schedule", params=prms)

    r = session.post('https://medbox.ru/2016/Schedule/LpuSearch',
                     data={"CityName": prms["city"]})
    r = session.post("https://medbox.ru/2016/Schedule/SpecSearch",
                     data={"connAlias": prms["alias"], "s_lpu": prms["dept"], "lid": prms["lid"]})
    r = session.post("https://medbox.ru/2016/Schedule/DocSearch",
                     data={"connAlias": prms["alias"], "depNum": prms["dept"], "spec": "-999"})

    # change to json lib
    schedule = eval(str(bs(r.content, 'lxml').text))

    medspec_list = set()
    for s in schedule:
        medspec_list.add(s['medspec'])
    medspec_list = tuple(sorted(medspec_list))

    print("\nВыберите специальность :")
    for n, s in enumerate(medspec_list, 1):
        print(n, '->', s)

    medspec = medspec_list[int(input())-1]

    doctors_list = []
    for s in schedule:
        if s['medspec'] == medspec and s['freetime'] > 0:
            doctors_list.append(s)
            print(s['medspec'], s['name'], "\nСвободных мест:", s['freetime'], '\n')

    return doctors_list, medspec


if __name__ == "__main__":
    get_schedule()
