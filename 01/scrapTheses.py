# -*- coding: utf8 -*

__authot__ = 'Dominika Draesslerová'

import requests
from bs4 import BeautifulSoup as b

'''
final data are in format [(values),(values),(values),...]

scrap final theses from theses.cz

'''

num_of_works = 10
base_url = 'https://theses.cz'
url = base_url+'/th_search/catalogue?prac=th54;fak=th5453;search=Vyhledat;start='

university_name = 'Janáčkova akademie múzických umění v Brně'
faculty_name = 'JAMU - Divadelní fakulta'

#   output containers
data = []
links = []

#   load new pages with theses and save links

for i in range(num_of_works//10):
    #   get html
    page_code = requests.get(url+str(i))
    page_code = b(page_code.content,"html.parser")

    #   get theses element
    theses = page_code.find_all('div',class_='vyh_polozka')
    
    #   get link of these for next scrapping
    for these in theses:
        link = these.a['href']
        links.append(link)


# load each thesis
for link in links:
    #   get html
    page_code = requests.get(base_url+str(link))
    page_code = b(page_code.content,"html.parser")

    #   scrap informations
    tittle = page_code.find(class_='th-title').get_text()
    author = page_code.find(class_='th-autor').get_text()
    kind_of_work = page_code.find(class_='typ-prace').get_text()
    study_field = page_code.select_one('#th-sloupec > div:nth-child(1) > p > em').get_text().split(' / ')
    date = page_code.select_one('#metadata > div:nth-child(10) > div > ul > li:nth-child(1) > b').get_text()[1:]
    div = page_code.find('div',class_='medium-5 columns')
    leader = div.find_all('li')[1].get_text()[10:]
    oponent = div.find_all('li')[2].get_text()[10:]

    #   add row
    data.append( (tittle,author,kind_of_work,date,leader,oponent,study_field) )

with open('data.csv','w') as file:
    file.write(str(data))

    
