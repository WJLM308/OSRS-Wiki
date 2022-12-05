#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

wiki = 'https://oldschool.runescape.wiki/w/Module:200mxp/data'
wiki_contents = BeautifulSoup(requests.get(wiki).content, 'html.parser')
wiki_contents = wiki_contents.find_all('span')
entries = []
for i in wiki_contents:
    if i.get('class')==['mi']:
        entries += i
table = np.reshape(entries, (24, 4))
print('old data:')
print(table)
print()
url = 'https://secure.runescape.com/'
acc_type = ['m=hiscore_oldschool/', 'm=hiscore_oldschool_ironman/', 'm=hiscore_oldschool_ultimate/', 'm=hiscore_oldschool_hardcore_ironman/']
skill = [str(i+1) if i!=23 else '0' for i in range(24)]
for i,x in enumerate(skill):
    if x=='0':
        threshold = 4600000000
    else:
        threshold = 200000000
    for j,y in enumerate(acc_type):
        last = True
        extra_pages = 0
        while last:
            exp = 0
            page = BeautifulSoup(requests.get(url+y+'overall?table='+x+'&page='+str(int(table[i][j])//25+1+extra_pages)).content, 'html.parser')
            hiscores=page.find_all('td')
            if extra_pages == 0:
                start = int(table[i][j])%25
            else:
                start = 0
            exp = [int(hiscores[4*k+7].text.strip().replace(',','')) for k in range(start,24)]
            indices = [x for x in exp if x < threshold]
            if len(indices) != 0:
                print(url+y+'overall?table='+x+'&page='+str(int(table[i][j])//25+1+extra_pages))
                diff = (24-len(indices))-int(table[i][j])%25+25*extra_pages
                table[i][j] = str(int(table[i][j])+diff)
                print(table[i][j]+' (+'+str(diff)+')')
                last = False
            else:
                extra_pages += 1
print()
print('new data:')
print(table)

