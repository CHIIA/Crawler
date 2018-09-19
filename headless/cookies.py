# encoding=utf-8

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException,ElementNotVisibleException,WebDriverException,UnexpectedAlertPresentException
from selenium.webdriver.support.ui import Select
from time import sleep
import re
import math
import json
import logging
from datetime import datetime
import cgi
from pipeline import process_item
from dateutil.parser import parse
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(levelname)s - %(message)s')#,filename='./logs/{}.log'.format(datetime.now()))
logging.getLogger("selenium").setLevel(logging.CRITICAL)  # 将selenium的日志级别设成DEBUG，太烦人

formatter = logging.Formatter(
                              '%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')



anuID=[
       {'id':'u6274652','psw':'ly_game219'},
       ]

GATEWAY = 'ANULIB'

queryTerms = '((chin* or hong kong)) and (( (residential or site or commercial) and (casino resort or island or hotel or apartment or park or estate or property) and (group or firm or company or board or entitys) and (transaction* or purchase* or sale or sold or buy) ) or ( (uranium or wind or gold or solar or ore or copper or energy or alumina or iron or lead or coal or oil) and (bonds or acquisition or merge or purchase or sale or stake or equity) and (million* or billion* or B or M) and (operations or mining or firm or company)) or ( (dairy or cheese or butter or milk or bread or wine) and (sold or buy or sale or equity or stake or merge or acquire) and (brand or company or business or group or firm or board) and (million* or billion* or B or M))) not (terrorism or war or navy or stock market or share market or Wall St or Wall Street or Forex or Stock Exchange or rst=asxtex) and re=austr'
queryPeriod = 'In the last 5 years'

#Check Platform to load chromedriver
if os.name == 'nt':
	chrome_driver = os.getcwd() +"/chromedriver/win_chromedriver.exe"
elif os.name =='posix':
	chrome_driver = os.getcwd() +"/chromedriver/linux_chromedriver"
#else:
#    chrome_driver = os.getcwd() +"/chromedriver/mac_chromedriver"


#login by using headless chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)



def loginFectiva(browser,account,pwd):
    FLAG_LOGIN = False
    while not FLAG_LOGIN:
        try:
            
            browser.get("http://library-admin.anu.edu.au/tools/factiva-redirect")
            
            if GATEWAY == 'OUTSIDE':
                logger.info("Gateway: OUTSIDE")
                wait = WebDriverWait(browser, 5)
                anuID = wait.until(EC.presence_of_element_located((By.ID, 'requester')))
                anuID.send_keys(account)
                password = browser.find_element_by_id('requesteremail')
                password.send_keys(pwd)
                browser.get_screenshot_as_file("logs/pre-login.png")
                password.send_keys(Keys.RETURN)
            elif GATEWAY == 'ANULIB':
                logger.info("Gateway: ANULIB")
            else:
                logger.error("Please Set Cookie Gateway!")
           
            wait = WebDriverWait(browser, 40)
            browser.get_screenshot_as_file("logs/login.png")
            btn = wait.until(EC.presence_of_element_located((By.ID, 'btnSearchBottom')))
            #swith from smart search to fix search
            #switch = browser.find_element_by_id("switchbutton")
            #switch.click()
            sleep(1)
            input = browser.find_element_by_id('ftx')
            input.send_keys(queryTerms)
            #select searching date
            select = Select(browser.find_element_by_name('dr'))
            #select.select_by_index(index)
            select.select_by_visible_text(queryPeriod)
            #select.select_by_value(value)
            search_button = browser.find_element_by_id('btnSearchBottom')
            search_button.click()
            headlineFrame = wait.until(EC.presence_of_element_located((By.ID, 'headlineFrame')))
            browser.get_screenshot_as_file("logs/search.png")
            FLAG_LOGIN = True
        except NoSuchElementException:
            logger.error('No Element during login')
            browser.close()
        except ElementNotVisibleException:
            logger.error('Not Visible during login')
            browser.close()
        except TimeoutException:
            logger.error('Timeout during login')
            browser.get_screenshot_as_file("logs/capture.png")
            #browser.close()
    list_cookies = browser.get_cookies()
    cookies=dict()
    for item in list_cookies:
        cookies[item['name']] = item['value']

    return json.dumps(cookies)

def getStatus(browser):
    #Compute the total pages we need to download
    
    pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
    duplicate = browser.find_element_by_id('dedupSummary').text
    duplicate = int(re.match('Total duplicates: (.*)',duplicate).group(1))
    currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
    articlesInThisPage = int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(2)) - int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1)) + 1
    totalPages = math.ceil((int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(3))- duplicate)/100.0)-1
    nextPageStart = int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(2))+1
    totalWebNews = browser.find_element_by_xpath('//span[@data-channel="Website"][1]/a/span[@class="hitsCount"]').text.replace(',','')
    totalWebNews = int(re.search(r'\((.*)\)',totalWebNews).group(1))
    totalBlogs = browser.find_element_by_xpath('//span[@data-channel="Blog"][1]/a/span[@class="hitsCount"]').text.replace(',','')
    totalBlogs = int(re.search(r'\((.*)\)',totalBlogs).group(1))
    
    totalArticles = browser.find_element_by_xpath('//span[@data-channel="All"][1]/a/span[@class="hitsCount"]').text.replace(',','')
    totalArticles = int(re.search(r'\((.*)\)',totalArticles).group(1))
    totalArticles = totalArticles - totalBlogs - totalWebNews
    '''Minus WebNews'''

    return currentPage,totalPages,duplicate,nextPageStart,totalArticles,articlesInThisPage

def getArticleInfo(browser,id):
    headline = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/a'.format( id ))
    documentID = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/div[3]'.format(id)).text
    documentID =  re.search(r'\(Document (.*)\)',documentID).group(1)
    documentType = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/img'.format(id)).get_attribute('title')
    leadFields = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/div[@class="leadFields"]'.format(id)).text.split(',')
    author = leadFields[0]
    date = leadFields[1]
  

    return headline,date,author,documentID,documentType
def saveCheckPoint(checkpoint):
    f=open('checkpoint/checkpoint.json','w')
    json.dump(checkpoint,f)
    f.close()
    logger.info('Save checkpoint at {}'.format(checkpoint))
def loadCheckPoint():
    try:
        f=open('checkpoint/checkpoint.json','r')
        checkpoint = json.load(f)
        f.close()
        logger.info('Load checkpoint from file: {}'.format(checkpoint))
    except:
        logger.info('No checkpoint has been founded, Create a new checkpoint!')
        checkpoint = {'Dowjones':0, 'Publication':0, 'Website': 0}

    return checkpoint

def crawlFectiva(browser,checkpoint):

#select = Select(browser.find_element_by_name('hso'))
#select.select_by_visible_text('Sort by: Oldest first')

    for source in ['Dowjones','Publication']:
        dataChannel = browser.find_element_by_xpath('//span[@data-channel="{}"]'.format(source))
        dataChannel.click()
        logger.info('Start source from:{}...'.format(source))
        wait = WebDriverWait(browser, 10)
        btn = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="tabOn"][@data-channel="{}"]'.format(source))))
        
        #Compute the total pages we need to download
        currentPage,totalPages,duplicate,nextPageStart,totalArticles,articlesInThisPage = getStatus(browser)
        #Load checkpoint
	checkpoint = loadCheckPoint()
        logger.info('S Total pages:{} , currentAt:{} , checkPointAt:{}'.format(totalPages,currentPage,checkpoint[source]))
        while currentPage != totalPages or checkpoint[source]!=currentPage or totalPages == 0:
            logger.info('Total pages:{} , currentAt:{} , checkPointAt:{}'.format(totalPages,currentPage,checkpoint[source]))
            for i in range(abs(checkpoint[source] - currentPage)):
                #Compute the total pages we need to download
                currentPage,totalPages,duplicate,nextPageStart,totalArticles,articlesInThisPage = getStatus(browser)
                logger.info('Skip Page To checkPoint...Total pages:{} , currentAt:{} , checkPointAt:{}'.format(totalPages,currentPage,checkpoint[source]))
                btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
                btn_nextpage.click()
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[@class="headline"][1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))


            #Compute the total pages we need to download
            currentPage,totalPages,duplicate,nextPageStart,totalArticles,articlesInThisPage = getStatus(browser)

            for id in range(1,articlesInThisPage + 1):
                
                headline,date,author,documentID,documentType = getArticleInfo(browser,id)
         
                if documentType == 'Factiva Licensed Content':
                    logger.info('{:.1%} Get {} of {} in page {}.Totally {} pages {} articles'.format((currentPage*100+id)/float(totalArticles),id,articlesInThisPage, currentPage,totalPages,totalArticles))
                    
                    logger.debug('id:{}, documentID:{}, Headline:{}, date:{}, author:{} '.format(id,documentID,headline.text,date,author))
                    headline.click()
                    wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="artHdr1"]/span[1]'), 'Article {}'.format(currentPage * 100 + id) ))
                    articleHtml = browser.find_element_by_xpath('//div[@class="article enArticle"]')
                    title =headline.text
                    content = articleHtml.get_attribute('innerHTML')
                    try:
                    	date = parse(date).strftime('%Y-%m-%d')
                    	crawldate = parse(str(datetime.now())).strftime('%Y-%m-%d')
                    	url = ''
                    	process_item(documentID,title,author,content,date,crawldate,url)
                    except:
			pass
                    sleep(1)
                if documentType == 'HTML':
                    pass
                    '''
                    logger.info('{:.1%} Get {} of 100 in page {}.Totally {} pages {} articles'.format((currentPage*100+id)/totalArticles,id, currentPage,totalPages,totalArticles))
                    headline.click()
                    window_main = browser.window_handles[0]
                    window_download = browser.window_handles[-1]
                    browser.switch_to_window(window_download)
                    sleep(4)
                    file_object = open('data/{}.html'.format(documentID), "w")
                    file_object.write(browser.page_source)
                    file_object.close()
                    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                    browser.switch_to_window(window_main)
                    '''
                    

         
              #sometimes recaptcha occurs here
              #view next page
            
            if currentPage == totalPages:
                break
            
            checkpoint[source] = currentPage
            saveCheckPoint(checkpoint)

            btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
            btn_nextpage.click()
            wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[@class="headline"][1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))




while 1:
	checkpoint = loadCheckPoint()
	loginFectiva(browser,'','')
	try:
    		crawlFectiva(browser,checkpoint)
		break;
	except TimeoutException:
		logger.error('Timeout during crawling pages')
	except UnexpectedAlertPresentException:
    		logger.error('Fectiva alert:We are unable to process your request at this time.  Please try again in a few minutes.')
logger.info('Finish!')
browser.close()


#print(cookie)
logger.info("Get Cookies Finish!( Num:%d)" % len(cookie))
