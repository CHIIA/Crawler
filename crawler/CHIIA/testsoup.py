'''
from bs4 import BeautifulSoup
with open('logs/search.html','r') as f:
	soup = BeautifulSoup(f.read(),"html.parser")

for item in soup.find_all("a","enHeadline"):
    url = item.get('href')
    print(url)
    print(item.string)
    end = url.rfind('/')
    print(url[:end])
'''
import re

f = open(r'raw/1.html','rb')
content = f.read().decode('utf-8')
f.close()
s=re.search(r'doLinkPost\(\".*\,\"(.*)\"\,\"(.*)"\)',content)


print(s.group(1),'\n\n',s.group(2))
