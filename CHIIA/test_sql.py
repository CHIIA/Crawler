import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "lygame218", "NLP", charset='utf8' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# SQL 插入语句
item = dict()
item['_id'] ='id12'
item['Title']='title'
item['PostDate']='1993-02-14'
item['CrawlDate'] ='1992-02-15'
item['Url']='gttpo://1231'
sql = "insert into NLP_ARTICLE(ID,title,author,content,date,crawldate,url) values('%s','%s','%s','%s','%s','%s','%s')"
params =(item['_id'], item['Title'], 'YangLu','./articles', item['PostDate'],item['CrawlDate'],item['Url'])
ss = sql % params
print(ss)
try:
   # 执行sql语句
   cursor.execute(sql % params)
   # 提交到数据库执行
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# 关闭数据库连接
db.close()
