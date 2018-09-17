# encoding=utf-8

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException,NoSuchElementException,ElementNotVisibleException,WebDriverException
from selenium.webdriver.support.ui import Select
from time import sleep
import re

import json
import logging




logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.CRITICAL)  # 将selenium的日志级别设成DEBUG，太烦人


anuID=[
       {'id':'u6274652','psw':'ly_game219'},
       ]

COOKIE_GETWAY = 'ANULIB'


#Check Platform to load chromedriver
if os.name == 'nt':
    chrome_driver = os.getcwd() +"/chromedriver/win_chromedriver.exe"
else:
    chrome_driver = os.getcwd() +"/chromedriver/mac_chromedriver"


#login by using headless chrome
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)



def get_cookie_with_login(account,pwd):
    FLAG_LOGIN = False
    while not FLAG_LOGIN:
        try:
            
            browser.get("http://library-admin.anu.edu.au/tools/factiva-redirect")
            wait = WebDriverWait(browser, 5)
            anuID = wait.until(EC.presence_of_element_located((By.ID, 'requester')))
            anuID.send_keys(account)
            password = browser.find_element_by_id('requesteremail')
            password.send_keys(pwd)
            browser.get_screenshot_as_file("logs/pre-login.png")
            password.send_keys(Keys.RETURN)
           
            wait = WebDriverWait(browser, 40)
            browser.get_screenshot_as_file("logs/login.png")
            btn = wait.until(EC.presence_of_element_located((By.ID, 'btnSearchBottom')))
            #swith from smart search to fix search
            switch = browser.find_element_by_id("switchbutton")
            switch.click()
            input = browser.find_element_by_id('ftx')
            input.send_keys('((chin* or hong kong)) and (( (residential or site or commercial) and (casino resort or island or hotel or apartment or park or estate or property) and (group or firm or company or board or entitys) and (transaction* or purchase* or sale or sold or buy) ) or ( (uranium or wind or gold or solar or ore or copper or energy or alumina or iron or lead or coal or oil) and (bonds or acquisition or merge or purchase or sale or stake or equity) and (million* or billion* or B or M) and (operations or mining or firm or company)) or ( (dairy or cheese or butter or milk or bread or wine) and (sold or buy or sale or equity or stake or merge or acquire) and (brand or company or business or group or firm or board) and (million* or billion* or B or M))) not (terrorism or war or navy or stock market or share market or Wall St or Wall Street or Forex or Stock Exchange or rst=asxtex) and re=austr')
            #select searching date
            select = Select(browser.find_element_by_name('dr'))
            #select.select_by_index(index)
            select.select_by_visible_text("In the last 2 years")
            #select.select_by_value(value)
            search_button = browser.find_element_by_id('btnSearchBottom')
            search_button.click()
            headlineFrame = wait.until(EC.presence_of_element_located((By.ID, 'headlineFrame')))
            browser.get_screenshot_as_file("logs/search.png")
            FLAG_LOGIN = True
        except NoSuchElementException:
            print('No Element')
            browser.close()
        except ElementNotVisibleException:
            print('Not Visible')
            browser.close()
        except TimeoutException:
            print('Timeout')
            browser.get_screenshot_as_file("logs/capture.png")
            #browser.close()
    list_cookies = browser.get_cookies()
    cookies=dict()
    for item in list_cookies:
        cookies[item['name']] = item['value']

    return json.dumps(cookies)

def get_cookie_without_login():
    FLAG_LOGIN = False
    while not FLAG_LOGIN:
        try:
            
            browser.get("http://library-admin.anu.edu.au/tools/factiva-redirect")
            wait = WebDriverWait(browser, 40)
            browser.get_screenshot_as_file("logs/login.png")
            btn = wait.until(EC.presence_of_element_located((By.ID, 'btnSearchBottom')))
            #swith from smart search to fix search
            switch = browser.find_element_by_id("switchbutton")
            switch.click()
            input = wait.until(EC.presence_of_element_located((By.ID, 'ftx')))
            input.send_keys('((chin* or hong kong)) and (( (residential or site or commercial) and (casino resort or island or hotel or apartment or park or estate or property) and (group or firm or company or board or entitys) and (transaction* or purchase* or sale or sold or buy) ) or ( (uranium or wind or gold or solar or ore or copper or energy or alumina or iron or lead or coal or oil) and (bonds or acquisition or merge or purchase or sale or stake or equity) and (million* or billion* or B or M) and (operations or mining or firm or company)) or ( (dairy or cheese or butter or milk or bread or wine) and (sold or buy or sale or equity or stake or merge or acquire) and (brand or company or business or group or firm or board) and (million* or billion* or B or M))) not (terrorism or war or navy or stock market or share market or Wall St or Wall Street or Forex or Stock Exchange or rst=asxtex) and re=austr')
            
            #select searching date
            select = Select(browser.find_element_by_name('dr'))
            #select.select_by_index(index)
            select.select_by_visible_text("In the last 2 years")
            #select.select_by_value(value)
            
            search_button = browser.find_element_by_id('btnSearchBottom')
            search_button.click()
            headlineFrame = wait.until(EC.presence_of_element_located((By.ID, 'headlineFrame')))
            browser.get_screenshot_as_file("logs/search.png")
            FLAG_LOGIN = True
        except NoSuchElementException:
            print('No Element')
            browser.close()
        except ElementNotVisibleException:
            print('Not Visible')
            browser.close()
        except TimeoutException:
            print('Timeout')
            browser.get_screenshot_as_file("logs/capture.png")
    #browser.close()
    list_cookies = browser.get_cookies()
    cookies=dict()
    for item in list_cookies:
        cookies[item['name']] = item['value']
    
    return json.dumps(cookies)


def getCookie(account,password):
    if COOKIE_GETWAY == 'ANULIB':
        print('Gateway: ANULIB')
        return get_cookie_without_login()
    elif COOKIE_GETWAY =='OUTSIDE':
        print('Gateway: OUTSIDE')
        return get_cookie_with_login(account,password)
    else:
        logger.error("Please Set Cookie Gateway!")


def getCookies():
    """ 获取Cookies """
    logger.info("Get cookie...")
    cookies = []
    

    # download the chrome browser from https://sites.google.com/a/chromium.org/chromebrowser/downloads and put it in the
    
    
    for elem in anuID:
        account = elem['id']
        password = elem['psw']
        cookie  =  getCookie(account,password)
        if cookie != None:
            cookies.append(cookie)
    else:
        logger.error("Please Set Cookie Gateway!")

    return cookies

def crawl(checkpoint):
    if checkpoint == None:
        checkpoint['Publication'] = 0
        checkpoint['Dowjones'] = 0
    for source in ['Dowjones']:
        
        
        dataChannel = browser.find_element_by_xpath('//span[@data-channel="{}"]'.format(source))
        dataChannel.click()
        print('Start source from:{}...'.format(source))
        wait = WebDriverWait(browser, 40)
        btn = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="tabOn"][@data-channel="{}"]'.format(source))))

        #Compute the total pages we need to download
        pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
        duplicate = browser.find_element_by_id('dedupSummary').text
        duplicate = int(re.match('Total duplicates: (.*)',duplicate).group(1))
        currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
        checkPointPage = checkpoint[source]
        totalPages = int((int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(3)) - duplicate)/100)-1
        
        while currentPage != totalPages or checkPointPage!=currentPage:
            print(currentPage,checkPointPage,totalPages)
            try:
                for i in range(abs(checkPointPage - currentPage)):
                    #Compute the total pages we need to download
                    pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
                    currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
                    nextPageStart = int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(2))+1
                    btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
                    btn_nextpage.click()
                    wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))
                
                
                #Compute the total pages we need to download
                pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
                currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
                nextPageStart = int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(2))+1
                totalPages = int((int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(3)) - duplicate)/100)
  

                
                selectAll =  browser.find_element_by_id("selectAll")
                selectAll.click()
                print('Now downloading:{} of {}, {}, Total duplicate:{}... '.format(currentPage,totalPages,pageInfo,duplicate))
                #click download(javascript)
                browser.execute_script("viewProcessing('../hp/printsavews.aspx?pp=Save&hc=All');")
                window_main = browser.window_handles[0]
                window_download = browser.window_handles[-1]
                browser.switch_to_window(window_download)
                wait.until(EC.presence_of_element_located((By.ID, 'navcontainer')))
                file_object = open('data/{}_page{}.html'.format(source,currentPage), "w")
                file_object.write(browser.page_source)
                file_object.close()
                browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                browser.switch_to_window(window_main)
                
                clearAll =  browser.find_element_by_id("clearAll")
                clearAll.click()
                #sometimes recaptcha occurs here
                #view next page
                if currentPage == totalPages:
                    break
                btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
                btn_nextpage.click()
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[@class="headline"][1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))
            
            
            except:
                print('Oops! Validation Code Occurs!')
                sleep(5)
                wait = WebDriverWait(browser, 500)
                valid = wait.until(EC.invisibility_of_element_located((By.XPATH,'//div[@id="recaptchapopupoverlay"]')))
                print('Pass recaptcha success!')
                #unselect all
                try:
                    clearAll =  browser.find_element_by_id("clearAll")
                    clearAll.click()
                except:
                    pass
                #view next page
                btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
                btn_nextpage.click()
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[@class="headline"][1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))


def crawl_publications(checkpoint):
    if checkpoint == None:
        checkpoint['Publication'] = 0
        checkpoint['Dowjones'] = 0
    for source in ['Publication']:
        dataChannel = browser.find_element_by_xpath('//span[@data-channel="{}"]'.format(source))
        dataChannel.click()
        print('Start source from:{}...'.format(source))
        wait = WebDriverWait(browser, 40)
        btn = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="tabOn"][@data-channel="{}"]'.format(source))))
        
        #Compute the total pages we need to download
        pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
        duplicate = browser.find_element_by_id('dedupSummary').text
        duplicate = int(re.match('Total duplicates: (.*)',duplicate).group(1))
        currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
        checkPointPage = checkpoint[source]
        totalPages = int((int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(3)) - duplicate)/100)-1
        while currentPage != totalPages or checkPointPage!=currentPage:
            print(currentPage,checkPointPage,totalPages)
            
            for i in range(abs(checkPointPage - currentPage)):
                #Compute the total pages we need to download
                pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
                currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
                nextPageStart = int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(2))+1
                btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
                btn_nextpage.click()
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[@class="headline"][1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))


            #Compute the total pages we need to download
            pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
            currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
            nextPageStart = int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(2))+1
            totalPages = int((int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(3)) - duplicate)/100)

            for id in range(1,100):
                
                headline = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/a'.format( id ))
                documentID = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/div[3]'.format(id)).text
                documentID =  re.search(r'\(Document (.*)\)',documentID).group(1)
                documentType = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/img'.format(id)).get_attribute('title')
                if documentType != 'Factiva Licensed Content':
                    continue
                print(currentPage * 100 + id,headline.text)
                headline.click()
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="artHdr1"]/span[1]'), 'Article {}'.format(currentPage * 100 + id) ))
                articleHtml = browser.find_element_by_xpath('//div[@class="article enArticle"]')
           
                file_object = open('data/{}.html'.format(documentID), "w")
                file_object.write(articleHtml.get_attribute('innerHTML'))
                file_object.close()
                    #sleep(1)# To fast will be banned

           


              #sometimes recaptcha occurs here
              #view next page
            if currentPage == totalPages:
                break
            btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
            btn_nextpage.click()
            wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[@class="headline"][1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))

def crawlWebNews(checkpoint):
    if checkpoint == None:
        checkpoint['Publication'] = 0
        checkpoint['Dowjones'] = 0
        checkpoint['Web News'] = 0
    for source in ['Web News']:
        dataChannel = browser.find_element_by_xpath('//span[@data-channel="{}"]'.format(source))
        dataChannel.click()
        print('Start source from:{}...'.format(source))
        wait = WebDriverWait(browser, 40)
        btn = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="tabOn"][@data-channel="{}"]'.format(source))))
        
        #Compute the total pages we need to download
        pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
        duplicate = browser.find_element_by_id('dedupSummary').text
        duplicate = int(re.match('Total duplicates: (.*)',duplicate).group(1))
        currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
        checkPointPage = checkpoint[source]
        totalPages = int((int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(3)) - duplicate)/100)-1
        while currentPage != totalPages or checkPointPage!=currentPage:
            print(currentPage,checkPointPage,totalPages)
            
            for i in range(abs(checkPointPage - currentPage)):
                #Compute the total pages we need to download
                pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
                currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
                nextPageStart = int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(2))+1
                btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
                btn_nextpage.click()
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[@class="headline"][1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))
            
            
            #Compute the total pages we need to download
            pageInfo = browser.find_element_by_xpath('//span[@class="resultsBar"]').text.replace(',','')
            currentPage = int(int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(1))/100)
            nextPageStart = int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(2))+1
            totalPages = int((int(re.search(r'Headlines (.*) - (.*) of (.*)',pageInfo).group(3)) - duplicate)/100)
            
            for id in range(1,100):
                
                headline = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/a'.format( id ))
                documentType = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/img'.format(id)).get_attribute('title')
                print('dtype:',documentType)
                documentID = browser.find_element_by_xpath('//div[@id="headlines"]/table/tbody/tr[{}]/td[3]/div[3]'.format(id)).text
                documentID =  re.search(r'\(Document (.*)\)',documentID).group(1)
                print(documentID)
                print(currentPage * 100 + id,headline.text)
                headline.click()
                
                '''
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="artHdr1"]/span[1]'), 'Article {}'.format(currentPage * 100 + id) ))
                articleHtml = browser.find_element_by_xpath('//div[@class="article enArticle"]')
                
                file_object = open('data/{}.html'.format(documentID), "w")
                file_object.write(articleHtml.get_attribute('innerHTML'))
                file_object.close()
                sleep(1)# To fast will be banned
                '''
            
            
            
            
            #sometimes recaptcha occurs here
            #view next page
            if currentPage == totalPages:
                break
            btn_nextpage = browser.find_element_by_xpath('//a[@class="nextItem"]')
            btn_nextpage.click()
            wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@id="headlines"]/table/tbody/tr[@class="headline"][1]/td[@class="count"]'), '{}.'.format(nextPageStart) ))

cookie = getCookies()

checkpoint = {'Dowjones':3, 'Publication':5, 'Web News': 2}
#crawl(checkpoint)
crawl_publications(checkpoint)
browser.close()


#print(cookie)
logger.info("Get Cookies Finish!( Num:%d)" % len(cookie))
