# encoding=utf-8
import MySQLdb
import logging

logger = logging.getLogger('MYSQL')

logger.info('Start connect to Mysql')
db = MySQLdb.connect("localhost", "root", "root", "NLP", charset='utf8')



def process_item(id,title,author,content,date,crawldate,url):
    """ 判断item的类型，并作相应的处理，再入数据库 """
    
    try:
        sql = "insert into NLP_ARTICLE(ID,title,author,content,date,crawldate,url) values('%s','%s','%s','%s','%s','%s','%s')"
        params =(id, title, author,content, date,crawldate,url)
        # 执行sql语句
        cursor = db.cursor()
        cursor.execute(sql % params)
        # 提交到数据库执行
        db.commit()
        return 1
    except:
        # Rollback in case there is any error
        db.rollback()
        return 0
    # 关闭数据库连接



