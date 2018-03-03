# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class FectivaSpider(scrapy.Spider):
    name = 'fectiva'
    allowed_domains = ['factiva.com']
   
    
    def start_requests(self):
        post_data = "ftx=Australia"
        search_url = 'https://global-factiva-com.virtual.anu.edu.au/ha/default.aspx'
        post_header={}
        post_header["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8" 
        yield Request(url=search_url, method='POST',headers= post_header, body=post_data,
                          callback=self.parse)

    
    def parse(self, response):
        print(response.body)
        filename = 'index.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        pass
