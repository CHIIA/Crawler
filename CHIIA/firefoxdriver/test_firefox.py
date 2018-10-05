from selenium import webdriver
from selenium.webdriver.firefox.options import Options
firefox_options = Options()
#firefox_options.add_argument("-headless")
firefox_options.add_argument("--headless")
browser= webdriver.Firefox(firefox_options=firefox_options,executable_path=r'./geckodriver_linux')

url='http://www.baidu.com'
browser.get(url)
browser.get_screenshot_as_file("capture.png")
browser.close()

