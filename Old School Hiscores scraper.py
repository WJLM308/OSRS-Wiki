#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import numpy as np

# getting current table
wiki = 'https://oldschool.runescape.wiki/w/Module:200mxp/data'
wiki_contents = BeautifulSoup(requests.get(wiki).content, 'html.parser')
wiki_contents = wiki_contents.find_all('span')
entries = []
for i in wiki_contents:
    if i.get('class')==['mi']:
        entries += i
table = np.reshape(entries, (24, 4))
# printing current table
print('old data:')
print()
print(table)
print()

# here is where the actual Hiscore scraping begins -- a lot of annoying HTML parsing involved
print('(updating data; this may take a minute)')
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
        # this is the most complicated part -- essentially I am going from page to page, checking how many people have max xp
        while last:
            xp = 0
            page = BeautifulSoup(requests.get(url+y+'overall?table='+x+'&page='+str(int(table[i][j])//25+1+extra_pages)).content, 'html.parser')
            hiscores=page.find_all('td')
            if extra_pages == 0:
                start = int(table[i][j])%25
            else:
                start = 0
            xp = [int(hiscores[4*k+7].text.strip().replace(',','')) for k in range(start,24)]
            indices = [i for i in xp if i < threshold]
            # updating the table with new data
            if len(indices) != 0:
                print(url+y+'overall?table='+x+'&page='+str(int(table[i][j])//25+1+extra_pages))
                diff = (24-len(indices))-int(table[i][j])%25+25*extra_pages
                table[i][j] = str(int(table[i][j])+diff)
                print(table[i][j]+' (+'+str(diff)+')')
                last = False
            else:
                extra_pages += 1
# printing new table
print()
print('new data:')
print()
print(table)
print()

# putting the new table in an easy copy/paste format -- I realize that the following line is REALLY long, my apologies
formatting = ("-- skill = all, im, uim, hcim\nreturn {{\n\t['attack'] = {{{}, {}, {}, {}}},\n\t['defence'] = {{{}, {}, {}, {}}},\n\t['strength'] = {{{}, {}, {}, {}}},\n\t['hitpoints'] = {{{}, {}, {}, {}}},\n\t['ranged'] = {{{}, {}, {}, {}}},\n\t['prayer'] = {{{}, {}, {}, {}}},\n\t['magic'] = {{{}, {}, {}, {}}},\n\t['cooking'] = {{{}, {}, {}, {}}},\n\t['woodcutting'] = {{{}, {}, {}, {}}},\n\t['fletching'] = {{{}, {}, {}, {}}},\n\t['fishing'] = {{{}, {}, {}, {}}},\n\t['firemaking'] = {{{}, {}, {}, {}}},\n\t['crafting'] = {{{}, {}, {}, {}}},\n\t['smithing'] = {{{}, {}, {}, {}}},\n\t['mining'] = {{{}, {}, {}, {}}},\n\t['herblore'] = {{{}, {}, {}, {}}},\n\t['agility'] = {{{}, {}, {}, {}}},\n\t['thieving'] = {{{}, {}, {}, {}}},\n\t['slayer'] = {{{}, {}, {}, {}}},\n\t['farming'] = {{{}, {}, {}, {}}},\n\t['runecraft'] = {{{}, {}, {}, {}}},\n\t['hunter'] = {{{}, {}, {}, {}}},\n\t['construction'] = {{{}, {}, {}, {}}},\n\t['overall'] = {{{}, {}, {}, {}}},\n\t['update'] = '{}'\n}}")
print('reformatted text for pasting directly into Module:200mxp/data:')
print()
print(formatting.format(*table.reshape((96)).tolist(), date.today().strftime('%#d %B %Y')))

