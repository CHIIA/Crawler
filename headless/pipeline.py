import MySQLdb



db = MySQLdb.connect("localhost", "root", "lygame218", "NLP", charset='utf8')
    
def process_item(id,title,author,content,date,crawldate,url,source,type,text):
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
