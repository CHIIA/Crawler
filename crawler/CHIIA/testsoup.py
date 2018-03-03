from bs4 import BeautifulSoup
with open('logs/search.html','r') as f:
	soup = BeautifulSoup(f.read(),"html.parser")

for item in soup.find_all("a","enHeadline"):
    url = item.get('href')
    print(url)
    print(item.string)
    end = url.rfind('/')
    print(url[:end])
