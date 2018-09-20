# encoding=utf-8
import MySQLdb
from log import logger


logger.info('Start connect to Mysql')
db = MySQLdb.connect("localhost", "root", "root", "NLP", charset='utf8')
settings = {'id':None,'term':None,'startDate':None,'endDate':None}

def processItem(id,title,author,content,date,crawldate,url,source):
    """ put item into mysql database """
    
    try:
	content = MySQLdb.escape_string(content)
        sql = "insert into NLP_ARTICLE(ID,title,author,content,date,crawldate,url,source) values('%s','%s','%s','%s','%s','%s','%s','%s')"
        params =(id, title, author,content, date,crawldate,url,source)
	# excute sql command
        cursor = db.cursor()
        cursor.execute(sql % params)
        # commit changes
        db.commit()
        return 1
    except:
        # Rollback in case there is any error
#        db.rollback()
        return 0
    # shut donw database

def checkItemExist(id):
	sql = "select ID from NLP_ARTICLE where ID = '%s'" % id
	cursor = db.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	if result:
		return True
	else:
		return False

def loadSettings():
	for key in settings:
		sql = "select {} from NLP_SPIDER order by id DESC limit 1".format(key)
        	cursor = db.cursor()
		cursor.execute(sql)
		if key == 'startDate':
			full_date = (cursor.fetchone())[0]
			logger.info('Load settings: startDate = {}'.format(full_date))
			settings[key] = {'frd':full_date.day,'frm':full_date.month,'fry':full_date.year}
		elif key == 'endDate':
			full_date = (cursor.fetchone())[0]
			logger.info('Load settings: endDate = {}'.format(full_date))
			settings[key] = {'tod':full_date.day,'tom':full_date.month,'toy':full_date.year}
		else:
        		settings[key] = (cursor.fetchone())[0]
			logger.info('Load settings: {} = {}'.format(key,settings[key]))
	return settings
def getTaskID():
	sql = "select id from NLP_SPIDER order by id DESC limit 1"
	cursor = db.cursor()
        cursor.execute(sql) 
	id = (cursor.fetchone())[0]
	return id
def getDatabase():
	return db
def updateProgress(progress):
        sql = "update NLP_SPIDER set progress={}  where id = {}".format(progress,settings['id']) 
        cursor = db.cursor()
        cursor.execute(sql)
	db.commit() 
