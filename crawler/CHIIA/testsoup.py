
from bs4 import BeautifulSoup
with open('logs/search.html','r') as f:
	soup = BeautifulSoup(f.read(),"html.parser")

for item in soup.find_all("a","\\\"enHeadline\\\""):
    title = item.string
    articles_url='https://global-factiva-com.virtual.anu.edu.au' + item.get('href')[4:]
    print('Title: {}\nURL: {}\n'.format(title,articles_url))


'''
import re
from bs4 import BeautifulSoup

f = open(r'logs/search.html','rb')
content = f.read().decode('utf-8')
f.close()
soup = BeautifulSoup(content,"html.parser")
for item in soup.find_all(attrs = {"name": "_XFORMSTATE"}):
    xformstate = item.get('value')
print(xformstate)
'''


