# encoding=utf-8
from  pipeline import checkItemExist,loadSettings,updateProgress,getTaskID,getDatabase
from log import logger
res =checkItemExist('WC50042020180914ee9c0000g')
res = checkItemExist('xyz')
print(res)
print(loadSettings())
updateProgress(0.1)
print('Task:',getTaskID())
logger.info('test')

#process_item('u6274652','Test','YangLu','content','1993-02-14','1993-02-14','http://','Website')
