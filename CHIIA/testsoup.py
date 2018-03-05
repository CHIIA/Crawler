from dateutil.parser import parse
from bs4 import BeautifulSoup
from datetime import datetime as dt
import re
with open('articles/10.html','r') as f:
	soup = BeautifulSoup(f.read(),"html.parser")

print(str(soup.find("div","article")))
#    print(item.get('id'))
print(dt.today().strftime('%Y-%m-%d'))

f = open(r'articles/10.html','rb')
content = f.read().decode('utf-8')
find = re.search(r'<b>PD</b>&nbsp;</td><td>(.*)</td></tr>',content).group(1).split('<')[0]
print(find)
dst = parse('5 March 2018').strftime('%Y-%m-%d')
print(dst)
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


