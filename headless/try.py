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
from datetime import datetime
import cgi
from pipeline import processItem,checkItemExist,loadSettings,updateProgress
from dateutil.parser import parse
from log import logger
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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
browser.set_page_load_timeout(10)
browser.get("https://global.factiva.com/sb/default.aspx?lnep=hp")
print(browser.page_source)
browser.close()
