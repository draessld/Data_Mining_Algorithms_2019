# -*- coding: utf8 -*

__author__ = 'Dominika Draesslerová'

import requests
from bs4 import BeautifulSoup as b


url = 'https://www.volby.cz/'

#result sets
''' 
    vote_results(rok,okrsek,strana,pocet_hlasu_abs,pocet_hlasu_perc)
'''
vote_results = set()

''' 
    vote_sides()
'''
vote_sides = set()

''' 
    vote_summary(rok,okrsek,zapsani_volici,vydane_obalky,volebni_ucast,odevzdane_obalky,platne_hlasy)
'''
vote_summary = set()

'''
    candidates
'''
candidates = set()

page_code = requests.get(url)
page_code = b(page_code.content,"html.parser")

vote_years = ["2002","2006","2010","2014","2018"]
county = 92
counties=["1001","1002","1003","1004","1005","1006","1007","1008","1009","1010","1011","1012","1013","1014","1015","1016","1017","1018","1019","1020","1021","1022","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","3001","3002","3003","3004","3005","3006","3007","3008","3009","3010","3011","3012","3013","3014","3015","4001","4002","4003","4004","4005","5001","5002","5003","5004","5005","5006","5007","5008","5009","5010","5011","5012","5013","5014","5015","5016","5017","5018","6001","6002","6003","6004","6005","6006","7001","7002","7003","7004","7005","7006","8001"]

#   scrap vote results
for y in vote_years:
    if y == "2002":
        for i in range(1,county):
            #   summary information
            vote_page = b(requests.get(url+"pls/kv"+y+"/kv1111?xjazyk=CZ&xid=1&xdz=3&xnumnuts=5302&xobec=555134&xokrsek="+str(i)).content,"html.parser")
            sum_table = vote_page.find_all('table')[0].find_all('tr')[1].find_all('td')
            vote_summary.add((y,str(i),sum_table[0].get_text().replace('\xa0',''),sum_table[1].get_text().replace('\xa0',''),sum_table[2].get_text().replace('\xa0',''),sum_table[3].get_text().replace('\xa0',''),sum_table[4].get_text().replace("\xa0",'')))
            #   detail information
            detail_table = vote_page.find_all('table')[1].find_all('tr')[2:]
            for row in detail_table:
                tds = row.find_all('td')
                vote_results.add((y,str(i),tds[1].get_text().replace('\xa0',''),tds[2].get_text().replace('\xa0',''),tds[3].get_text().replace('\xa0','')))
    elif y == "2014" or y == "2018":
        for i in counties:
            #   summary information
            vote_page = b(requests.get(url+"pls/kv"+y+"/kv1111?xjazyk=CZ&xid=1&xdz=3&xnumnuts=5302&xobec=555134&xokrsek="+i+"&xstat=0&xvyber=1").content,"html.parser")
            tds = vote_page.find_all('table')[0].find_all('tr')[1].find_all('td')
            vote_summary.add((y,i,tds[0].get_text().replace('\xa0',''),tds[1].get_text().replace('\xa0',''),tds[2].get_text().replace('\xa0','').replace(',','.'),tds[3].get_text().replace('\xa0',''),tds[4].get_text().replace("\xa0",'')))
            #   detail information
            detail_table = vote_page.find_all('table')[1].find_all('tr')[2:]
            for row in detail_table:
                tds = row.find_all('td')
                vote_results.add((y,i,tds[1].get_text().replace('\xa0',''),tds[2].get_text().replace('\xa0',''),tds[3].get_text().replace('\xa0','').replace(',','.')))
    else:
        for i in range(1,county):
            #   summary information
            vote_page = b(requests.get(url+"pls/kv"+y+"/kv1111?xjazyk=CZ&xid=1&xdz=3&xnumnuts=5302&xobec=555134&xokrsek="+str(i)+"&xstat=0&xvyber=1").content,"html.parser")
            tds = vote_page.find_all('table')[0].find_all('tr')[1].find_all('td')
            vote_summary.add((y,str(i),tds[0].get_text().replace('\xa0',''),tds[1].get_text().replace('\xa0',''),tds[2].get_text().replace('\xa0','').replace(',','.'),tds[3].get_text().replace('\xa0',''),tds[4].get_text().replace("\xa0",'')))
            #   detail information
            detail_table = vote_page.find_all('table')[1].find_all('tr')[2:]
            for row in detail_table:
                tds = row.find_all('td')
                vote_results.add((y,str(i),tds[1].get_text().replace('\xa0',''),tds[2].get_text().replace('\xa0',''),tds[3].get_text().replace('\xa0','').replace(',','.')))

'''

#   scrap vote sides and their shortcuts
for y in vote_years:
    vote_sides_page = b(requests.get(url+"pls/kv"+y+"/kv34?xjazyk=CZ&xid=1").content,"html.parser")
    rows = vote_sides_page.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 3:
            vote_sides.add((tds[1].get_text(),tds[2].get_text()))
'''

#   scrap candidates
for y in vote_years:
    if y == "2002":
        candidates_page = b(requests.get(url+"pls/kv"+y+"/kv21111?xjazyk=CZ&xid=1&xv=11&xdz=3&xnumnuts=5302&xobec=555134").content,"html.parser")
        rows = candidates_page.find_all('tr')[2:]
        for row in rows:
            tds = row.find_all('td')[1:]
            a = []
            for td in tds:
                td = td.get_text().replace('\xa0',' ')
                a.append(td)
            candidates.add((y,'"'+a[0]+'"',a[1],'"'+a[2]+' '+a[3]+'"',a[4],'"'+a[5]+'"','"'+a[6]+'"',a[7].replace(' ',''),a[8].replace(',','.'),a[9],a[10]))

    else:
        candidates_page = b(requests.get(url+"pls/kv"+y+"/kv21111?xjazyk=CZ&xid=1&xv=11&xdz=3&xnumnuts=5302&xobec=555134&xstrana=0").content,"html.parser")
        rows = candidates_page.find_all('tr')[2:]
        for row in rows:
            tds = row.find_all('td')[1:]
            a = []
            for td in tds:
                td = td.get_text().replace('\xa0','')

                a.append(td)
                # rok,kandidatni_strana,poradove_cislo,jmeno,vek,navrhujici_strana,polititcka_prislusnost,pocet_hlasu_abs,pocet_hlasu_perc,poradi_zvol_nahradnika,mandat
            candidates.add((y,'"'+a[0]+'"',a[1],'"'+a[2]+'"',a[3],'"'+a[4]+'"','"'+a[5]+'"',a[6].replace(' ',''),a[7].replace(',','.'),a[8],a[9]))

with open('summary.csv','w') as f:
    f.write("rok;okrsek;zapsani_volici;vydane_obalky;volebni_ucast;odevzdane_obalky;platne_hlasy\n")
    for i in vote_summary:
        a = ''
        for j in i:
            if j == '-' or j == ' ':
                a += '"";'
            elif j == '00':
                a+= '0;'
            else:    
                a += j+';'
        f.write(a[:-1]+'\n')

'''

with open('sides.csv','w') as f:
    for i in vote_sides:
        a = ''
        for j in i:
            a +=  j[i]+', '
        f.write(a[:-2])
'''
with open('detail_votes.csv','w') as f:
    f.write("rok;okrsek;strana;pocet_hlasu_abs;pocet_hlasu_perc\n")
    for i in vote_results:
        a = ''
        for j in i:
            if j == '-' or j == ' ':
                a += '"";'
            else:    
                a += j+';'
        f.write(a[:-1]+'\n')

with open('candidates.csv','w') as f:
    f.write("rok;kandidatni_strana;poradove_cislo;jmeno;vek;navrhujici_strana;politika_prislusnost;pocet_hlasu_abs;pocet_hlasu_perc;poradi_zvol_nahradnika;mandat\n")
    for i in candidates:
        a = ''
        for j in i:
            if j == '-' or j == ' ':
                a += '"";'
            else:    
                a += j+';'
        f.write(a[:-1]+'\n')