# -*- coding: utf-8 -*-
import scrapy


class FectivaSpider(scrapy.Spider):
    name = 'fectiva'
    allowed_domains = ['factiva.com']
    start_urls = ['https://global-factiva-com.virtual.anu.edu.au/ha/default.aspx']
    

    def parse(self, response):
        print(response.body)
        filename = 'index.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        pass
