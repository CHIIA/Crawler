# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.http import FormRequest
from bs4 import BeautifulSoup




class FectivaSpider(scrapy.Spider):
    name = 'fectiva'
    allowed_domains = ['factiva.com','virtual.anu.edu.au']
    i=0
    
    def start_requests(self):
        post_data = "ftx=Australia"
        search_url = 'https://global-factiva-com.virtual.anu.edu.au/ha/default.aspx'
        body = "ftx=Chin*"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        yield FormRequest(url=search_url,formdata={'ftx': 'Chin*'},
                          callback=self.parse_search)
        
    def parse_article(self,response):
        self.i+=1
        filename = 'articles/%d.html' % i
        with open(filename, 'wb') as f:
            f.write(response.body)

    def parse_search(self, response):
        filename = 'logs/search.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        soup = BeautifulSoup(response.body,"html.parser")
        for item in soup.find_all("a","enHeadline"):
            title = item.string
            articles_url='https://global-factiva-com.virtual.anu.edu.au' + item.get('href')[2:]
            print('Title: {}\nURL: {}\n'.format(title,articles_url))
            yield Request(url=articles_url,callback=self.parse_article,dont_filter=True)


