import MySQLdb
import logging

logger = logging.getLogger('MYSQL')

logger.info('Start connect to Mysql')
db = MySQLdb.connect("localhost", "root", "lygame218", "NLP", charset='utf8')



def process_item(id,title,author,content,date,crawldate,url,source,type,text):
    """ 判断item的类型，并作相应的处理，再入数据库 """
    
    try:
        sql = "insert into NLP_ARTICLE(ID,title,author,content,date,crawldate,url) values('%s','%s','%s','%s','%s','%s','%s')"
        params =(id, title, author,content, date,crawldate,url)
        # 执行sql语句
        cursor = self.db.cursor()
        cursor.execute(sql % params)
        # 提交到数据库执行
        self.db.commit()
        return 1
    except:
        # Rollback in case there is any error
        self.db.rollback()
        return 0
    # 关闭数据库连接

