# -*- coding: utf-8 -*-

from datetime import datetime as dt
from dateutil.parser import parse

from bs4 import BeautifulSoup
import re
import urllib.request as urllib2

f = open('search.html','r')

soup = BeautifulSoup(f.read(),"html.parser")


def isDate(input):
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
    for m in month:
        if m in input:
            return True
    return False

#for i,(item, description) in enumerate(zip(soup.find_all("a","enHeadline"),soup.find_all("div","leadFields"))):
for item, description in zip(soup.find_all("a","\\\"enHeadline\\\""),soup.find_all("div","\\\"leadFields\\\"")):
   
    description = description.text.split(',')
    title = item.text
    author = description[0]
   
    if isDate(description[2]):
        date = parse(description[2]).strftime('%Y-%m-%d')
    else:
        date = parse(description[1]).strftime('%Y-%m-%d')
    print(description)
    articles_url='https://global-factiva-com.virtual.anu.edu.au' + item.get('href')[2:]
    
    find = re.search(r'accessionno=(.*)&fcpil',articles_url).group(1)
    print(find)
    print('Title: {}\nURL: {}\n author:{}\n data:{}\n'.format(title,articles_url,author,date))



'''s
for item in soup.find_all("a","\\\"enHeadline\\\""):
    title = item.string
    articles_url='https://global-factiva-com.virtual.anu.edu.au' + item.get('href')[4:]
    print('v',item.string)
'''
