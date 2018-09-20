# encoding=utf-8
from  pipeline import checkItemExist,loadSettings,updateProgress
res =checkItemExist('WC50042020180914ee9c0000g')
res = checkItemExist('xyz')
print(res)
print(loadSettings())
updateProgress(0.1)
#process_item('u6274652','Test','YangLu','content','1993-02-14','1993-02-14','http://','Website')
