import requests
from bs4 import BeautifulSoup as bs
from lxml import html

medurl = 'http://localhost:63342/Python/medbox.html?_ijt=m62u8anodnhumclsh8ttn3vsce'
r = requests.get(medurl,
                 headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'})
soup = bs(r.content, 'html.parser')

print(r.url)

# list of regions:
region = dict()
for s in soup.find('select', id = 'region_selector').findAll('option'):
    region[s.string.strip()] = s['value']
print(region)

# city = soup.find('span', id = 'hmao_town_list')
# nv86 = city.find('option', value = 'Нижневартовск')
# print(nv86)

# 'Ямало-Ненецкий автономный округ'
# str(soup('option', value = 89)[0].string).strip()

# print(soup.prettify())

# how to save page to local.html file :

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