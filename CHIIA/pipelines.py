# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from CHIIA.items import ArticleItem,PDFItem
from scrapy.http import FormRequest
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem


try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


import MySQLdb




class MongoDBPipleline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client["CHIIA"]
        self.Articles = db["Articles"]
    
    
    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        
        if isinstance(item, ArticleItem):
            try:
                self.Articles.insert(dict(item))
            except Exception:
                pass
        return item

class WebcrawlerScrapyPipeline(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "lygame218", "NLP", charset='utf8')

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
         
        if isinstance(item, ArticleItem):
            try:
                sql = "insert into NLP_ARTICLE(ID,title,author,content,date,crawldate,url) values('%s','%s','%s','%s','%s','%s','%s')"
                params =(item['_id'], item['Title'], item['Author'],item['Path'], item['PostDate'],item['CrawlDate'],item['Url'])
                # 执行sql语句
                cursor = self.db.cursor()
                cursor.execute(sql % params)
                # 提交到数据库执行
                self.db.commit()
            except:
                # Rollback in case there is any error
                self.db.rollback()
            # 关闭数据库连接
        return item

