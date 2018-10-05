# encoding=utf-8
import MySQLdb
import re
import numpy as np
from util import preprocessor
from util import vectorizer,transformer
from sklearn.linear_model import LogisticRegression
#from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support
import dill as pickle #use dill as pickle because pickle cannot handle function

db = MySQLdb.connect("localhost", "root", "root", "NLP", charset='utf8')


def writeModelLog(log):
        sql = "Update NLP_ML SET LOG = '{}' where id =1 ".format(log)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()

def writeModelAccuracy(accuracy):
        sql = "Update NLP_ML SET ACCURACY = '{}' where id =1 ".format(accuracy)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()



f = open('pretrained/model.pk','rb')
model = pickle.load(f)
log = 'Load pretrained model successfully.'
print(log)
writeModelLog(log) 
def modelPredict(hd,lp,td):
	token = model['test_token']	
	token.append(preprocessor(hd, lp, td))
	X = vectorizer.fit_transform(token)
	likelihood = model['classifier'].predict_proba(X)
	return likelihood[-1][1]

def modelTrain():
	#storage log as a string
	log = 'Loading data from database, it may take several minutes\n'
	writeModelLog(log)
	print(log)
	sql = "select ID, HD, LP, TD, STATUS from NLP_ARTICLE where source = 'dowjones' or source = 'publication' and date "
	cursor = db.cursor()
	cursor.execute(sql)
	articles = cursor.fetchall()
	print('There are {} articles in database.'.format(len(articles)))
	log += 'There are {} articles in database.'.format(len(articles))
	writeModelLog(log)
	token = []
	test_token = []
	test_ids = []
	y = []
	count = 0
	
	for article in articles:
		id, hd, lp, td, status = article
		log += 'now is preprocess article: {}\n'.format(count)
		print(count)
		writeModelLog(log)
		count+=1
		if status == 0:
			test_ids.append(id)
			test_token.append(preprocessor(hd, lp, td))
		else:
			token.append(preprocessor(hd, lp, td))
			y.append(2 - status)

	#test_token = model['test_token']
	#token = model['token']
	
	log += 'There are {} labeled articles, {} unlabeled articles.\n'.format(len(token), len(test_token))
	log += 'There are {} relevant articles, {} unrelevant articles.\n'.format(sum(y), len(y)-sum(y))
	writeModelLog(log)
	print('There are {} labeled articles, {} unlabeled articles.\n'.format(len(token), len(test_token)))
	print('There are {} relevant articles, {} unrelevant articles.\n'.format(sum(y), len(y)-sum(y)))

	text_vec = vectorizer.fit_transform(token)
	test_x = vectorizer.fit_transform(test_token)
	#word = vectorizer.get_feature_names()
	#print(word)
	#print(text_vec.toarray().shape)
	#idx = np.argmax(text_vec.toarray(),axis=1).astype(int)
	#print([word[id] for id in idx])
	msk = np.random.rand(len(y)) < 0.75
	train_x = text_vec[msk]
	dev_x = text_vec[~msk]
	y = np.array(y)
	train_y = y[msk]
	dev_y = y[~msk]

	log +='Now is training...Please wait\n'
	writeModelLog(log)
	classifer = LogisticRegression()
	classifer.fit(train_x, train_y)
	dev_preds = classifer.predict(dev_x)
	confusion = confusion_matrix(dev_y, dev_preds)
	acc_bow = accuracy_score(dev_y, dev_preds)
	precisions_bow, recalls_bow, f1_scores_bow, _ = precision_recall_fscore_support(dev_y, dev_preds)
	print('confusion matrix:\n{}'.format( confusion))
	print('\naccuracy: {:.4}'.format(acc_bow))
	print("\n{:>1} {:>4} {:>4} {:>4}".format("", "prec", "rec", "F1"))
	log += 'Finish traning, now start inference all articles in database, it may take some several minutes'
	log += 'confusion matrix:\n{}'.format( confusion)
	log += '\naccuracy: {:.4}'.format(acc_bow)
	log += "\n{:>1} {:>4} {:>4} {:>4}".format("", "prec", "rec", "F1")
	writeModelLog(log)
	for (idx, scores) in enumerate(zip(precisions_bow, recalls_bow, f1_scores_bow)):
		print("{:>1} {:.2f} {:.2f} {:.2f}".format(
			idx, scores[0], scores[1], scores[2]
		))
	test_preds_proba = classifer.predict_proba(test_x)

	log += 'Writing result into database...\n'
	writeModelLog(log)
	for i in range(len(test_ids)):
		sql =  "UPDATE NLP_ARTICLE SET likelyhood  = {} WHERE ID = '{}'".format(test_preds_proba[i][1], test_ids[i])
		cursor.execute(sql)
	db.commit()

	log += 'saving model now\n'
	writeModelLog(log)
	#save model
	model = dict()
	model['classifier'] = classifer
	model['vectorizer'] = vectorizer
	model['test_token'] = test_token[1:100]
	#save vectorizer
 	f = open('pretrained/model.pk','wb')
	pickle.dump(model, f)	
	f.close()
	#write log into database
	log += 'Finish!\n'
	writeModelAccuracy(acc_bow)
	writeModelLog(log)
modelPredict('','','')
