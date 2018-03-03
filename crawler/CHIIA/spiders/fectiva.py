# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.http import FormRequest

class FectivaSpider(scrapy.Spider):
    name = 'fectiva'
    allowed_domains = ['factiva.com']
   
    
    def start_requests(self):
        post_data = "ftx=Australia"
        search_url = 'https://global-factiva-com.virtual.anu.edu.au/ha/default.aspx'
        body = "ftx=Chin*"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        yield FormRequest(url=search_url,formdata={'ftx': 'Chin*'},
                          callback=self.parse)

    
    def parse(self, response):
        print(response.body)
        filename = 'index.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        pass
