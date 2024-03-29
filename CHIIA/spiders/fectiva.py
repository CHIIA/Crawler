# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime as dt
import time
from dateutil.parser import parse
from scrapy.http import Request
from scrapy.http import FormRequest
from bs4 import BeautifulSoup
import re
from CHIIA.items import ArticleItem,PDFItem
import logging
#html to pdf
import pdfkit
import weasyprint
from scrapy.utils.project import get_project_settings
from xhtml2pdf import pisa
from CHIIA.cookies import cookie


logger = logging.getLogger(__name__)

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO


def isDate(input):
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
    for m in month:
        if m in input:
            return True
        return False


class FectivaSpider(scrapy.Spider):
    name = 'fectiva'
    allowed_domains = ['factiva.com','virtual.anu.edu.au']
    settings = get_project_settings()
    page = 0
    #i=0
    
    # Utility function
    def convertHtmlToPdf(self,sourceHtml, outputFitimelename):
        # open output file for writing (truncated binary)
        resultFile = open(outputFilename, "w+b")

        # convert HTML to PDF
        pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile) # file handle to recieve result
        # close output file
        resultFile.close()                 # close output file
        # return True on success and False on errors
        return pisaStatus.err

    def start_requests(self):
        post_data = "ftx=Australia"
        search_url = 'https://global-factiva-com.virtual.anu.edu.au/ha/default.aspx'
        ftx = '((chin* or hong kong)) and (( (residential or site or commercial) and (casino resort or island or hotel or apartment or park or estate or property) and (group or firm or company or board or entitys) and (transaction* or purchase* or sale or sold or buy) ) or ( (uranium or wind or gold or solar or ore or copper or energy or alumina or iron or lead or coal or oil) and (bonds or acquisition or merge or purchase or sale or stake or equity) and (million* or billion* or B or M) and (operations or mining or firm or company)) or ( (dairy or cheese or butter or milk or bread or wine) and (sold or buy or sale or equity or stake or merge or acquire) and (brand or company or business or group or firm or board) and (million* or billion* or B or M))) not (terrorism or war or navy or stock market or share market or Wall St or Wall Street or Forex or Stock Exchange or rst=asxtex) and re=austr'
        dr = {'LastDay':'LastDay','LastWeek':'LastWeek','Last3Months':'Last3Months','Last6Months':'Last6Months','LastYear':'LastYear','Last2Year':'Last2Year','Last5Year':'Last5Year'}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        yield FormRequest(url=search_url,formdata={'ftx': ftx, 'dr':dr['Last5Year']},
                          callback=self.parse_search)
    

    def parse_redirect(self,response):
        #self.i+=1
        redirect_url = 'https://global-factiva-comtime.virtual.anu.edu.au/ga/default.aspx'
        
        #print('meta::',response.meta)
        
        articleitems = ArticleItem()
        articleitems['_id'] = response.meta['_id']
        articleitems['Title'] = response.meta['Title']
        #articleitems['Text'] =str(soup.find("div","article"))
        articleitems['PostDate'] = response.meta['Date']
        articleitems['CrawlDate'] = dt.today().strftime('%Y-%m-%d')
        articleitems['Url'] =  response.request.url
        articleitems['Path'] = '{}.pdf'.format(response.meta['_id'])
        articleitems['Author'] = response.meta['Author']
        print('[Important] article get from page:',response.meta['Page'])
        logger.info('[Important] article get from page:{}'.format(response.meta['Page']))
        yield articleitems
        '''
        filename = 'title-id.txt'
        with open(filename, 'a') as f:
            line = '{} - {}\n'.format(articleitems['_id'],articleitems['Title'])
            f.write(line)
        '''
        
        key=re.search(r'doLinkPost\(\".*\,\"(.*)\"\,\"(.*)"\)',response.body.decode('utf-8'))
        if key:
            xformstate = key.group(1)
            xformsesstate = key.group(2)
            yield FormRequest(url=redirect_url,formdata={'_XFORMSTATE':xformstate ,'_XFORMSESSSTATE':xformsesstate},callback=self.parse_article)
        else:
            options = {
                'page-size': 'Letter',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
		'load-error-handling': 'ignore',
                'quiet': '',
		'no-print-media-type':'',
		
            }
            config = pdfkit.configuration(wkhtmltopdf = '/usr/bin/wkhtmltopdf')
            #logger.info('Try to get PDF from: {}'.format(response.meta['redirect_urls']))
            #options = {'cookie': cookie}
            #pdfkit.from_url(response.body,'./articles/{}.pdf'.format(articleitems['_id']))
            try:
            	logger.info('save html To {}/{}.pdf'.format(self.settings['FILES_STORE'],articleitems['_id']))
            	pdfkit.from_string(response.body.decode('utf-8'),'{}/{}.pdf'.format(self.settings['FILES_STORE'],articleitems['_id']),options = options)
            except:
            	logger.info('wkhtml error')
            #weasyprint.HTML(string=response.body.decode('utf-8')).write_pdf('./articles/{}.pdf'.format(articleitems['_id']))
            #self.convertHtmlToPdf(response.body.decode('utf-8'),'{}/{}.pdf'.format(self.settings['FILES_STORE'],articleitems['_id']))
    def parse_article(self,response):
        content = response.body.decode('utf-8')
        soup = BeautifulSoup(content,"html.parser")
        
        
        '''
        articleitems = ArticleItem()
        articleitems['_id'] = soup.find("div","article").get('id').split('-')[1]
        articleitems['Title'] = soup.find("span","enHeadline").getText()
        articleitems['Text'] =str(soup.find("div","article"))
        date_str = re.search(r'<b>PD</b>&nbsp;</td><td>(.*)</td></tr>',content).group(1).split('<')[0]
        articleitems['PostDate'] =parse(date_str).strftime('%Y-%m-%d')
        articleitems['CrawlDate'] = dt.today().strftime('%Y-%m-%d')
        articleitems['Class'] = 'UNK'
        '''
        #logger.info('Start crawing:{}...'.format(articleitems['Title']))
        #print('id:',articleitems['_id'],'title: ',articleitems['Title'])
 
 
        pdfitem = PDFItem()
        pdfitem['_id'] = soup.find("div","article").get('id').split('-')[1]
        pdfitem['Title'] = soup.find("span","enHeadline").getText()
        pdfitem['url'] = 'https://global-factiva-com.virtual.anu.edu.au/pps/default.aspx?pp=PDF&ppstype=Article'
        pdfitem['Xformstate'],_ = self.get_formbody(content)
        pdfitem['SessionDto'] = re.search(r'sessionDto:\'(.*)\',isAdmin',content).group(1)
        #download pdfitem through filepipeline
        #yield pdfitem
        
        hdl = [{0:pdfitem['_id'],1:0,3:{0:'article'},5:'',6:1,10:0,11:0}]
        #yield FormRequest(url=item['url'],formdata={'_XFORMSTATE':item['Xformstate'] ,'_XFORMSESSSTATE':item['SessionDto'], 'hdl' : str(hdl)},dont_filter=True)
        logger.info('yield!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        yield FormRequest(url=pdfitem['url'],formdata={'_XFORMSTATE':pdfitem['Xformstate'] ,'_XFORMSESSSTATE':pdfitem['SessionDto'], 'hdl' : str(hdl)},dont_filter=True, callback=self.save_PDFfile, meta={'filename': pdfitem['_id']})
        
        #yield articleitems
        '''
        filename = 'articles/%d.html' % self.i
        with open(filename, 'wb') as f:
            f.write(response.body)
        '''
    
    def save_PDFfile(self,response):
        #print(response.meta['filename'])
       
        filename = str(response.meta['filename'])
        logger.info('[save pdf] filename: {}'.format(filename))
        buf = BytesIO(response.body)
        buf.seek(0)
        path = '{}/{}.pdf'.format(self.settings['FILES_STORE'],filename)
        with open(path, 'wb') as f:
            f.write(buf.getvalue())

    def get_formbody(self,response_body):
        soup = BeautifulSoup(response_body,"html.parser")
        xformstate = None
        xformsesstate = None
        for item in soup.find_all(attrs = {"name": "_XFORMSTATE"}):
            if item.get('value') != '':
                xformstate = item.get('value')
        for iitem in soup.find_all(attrs = {"name": "_XFORMSESSSTATE"}):
            if item.get('value') != '':
                xformsesstate = item.get('value')
        return xformstate,xformsesstate

    def parse_search(self, response):
        '''
        filename = 'logs/search.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        while 1:
            print('save a sample')
        '''
        if 'Page' in response.meta:#update session state
            print('[Important] page',response.meta['Page'])
            #logger.info('[Important] Response from page: {}'.format(response.meta['Page']))
        soup = BeautifulSoup(response.body.decode('utf-8'),"html.parser")
        
        for item, description in zip(soup.find_all("a","enHeadline"),soup.find_all("div","leadFields")):
            description = description.text.split(',')
            info = dict()
            if 'Page' in response.meta:
                info['Page'] = response.meta['Page']
            else:
                info['Page'] = 0
            info['Title'] = item.text
            info['Author'] = description[0]
            if isDate(description[2]):
                info['Date'] = parse(description[2]).strftime('%Y-%m-%d')
            else:
                info['Date'] = parse(description[1]).strftime('%Y-%m-%d')
            info['Articles_url']='https://global-factiva-com.virtual.anu.edu.au' + item.get('href')[2:]
            match = re.search(r'accessionno=(.*)&fcpil',info['Articles_url'])
            if match:
                info['_id'] = match.group(1)
            
            #print('Title: {}\nURL: {}\n'.format(title,articles_url))
            if 'Page' in response.meta:            
                print('[Request] request article from search page:',info['Page'])
            yield Request(url=info['Articles_url'], callback=self.parse_redirect, meta = info, dont_filter=True)
        for item, description in zip(soup.find_all("a","\\\"enHeadline\\\""),soup.find_all("div","\\\"leadFields\\\"")):
            description = description.text.split(',')
            info = dict()
            if 'Page' in response.meta:
                info['Page'] = response.meta['Page']
            else:
                info['Page'] = 0
            info['Title'] = item.text
            info['Author'] = description[0]
            if isDate(description[2]):
                info['Date'] = parse(description[2]).strftime('%Y-%m-%d')
            else:
                info['Date'] = parse(description[1]).strftime('%Y-%m-%d')
                                     
            info['Articles_url']= 'https://global-factiva-com.virtual.anu.edu.au' + item.get('href')[4:]
            match = re.search(r'accessionno=(.*)&fcpil',info['Articles_url'])
            if match:
                info['_id'] = match.group(1)
            if 'Page' in response.meta:            
                print('[Request] request article from search page:',info['Page'])
            yield Request(url=info['Articles_url'], callback=self.parse_redirect, meta = info, dont_filter=True)
        '''
        #find next_page start number
        find = re.search(r'viewNext.*viewNext\(\'(\d*)\'\);',response.body.decode('utf-8'))
        if find != None:
            next_page = find.group(1)
        else if re.search(r'viewNext\(\'(\d*)\'\);',response.body.decode('utf-8')).group(1):
            next_page = re.search(r'viewNext\(\'(\d*)\'\);',response.body.decode('utf-8')).group(1)
        
        logger.info('Current crawling page: {}'.format(next_page))
        '''
        #find xformstate and xformsesstate
        xformstate,xformsesstate = self.get_formbody(response.body.decode('utf-8'))
        if xformstate and xformsesstate != None:#update session state
            self.xformstate = xformstate
            self.xformsesstate = xformsesstate
        page_url = 'https://global-factiva-com.virtual.anu.edu.au/services/ajaxservice.aspx'
        
       
       
       
        if self.page ==0:
            for x in range(1,2000):
                time.sleep(10)
                self.page += 1
                logger.info('yield page {} request'.format(self.page))
                yield FormRequest(url=page_url,formdata={'_XFORMSTATE': self.xformstate ,
                                  '_XFORMSESSSTATE': self.xformsesstate,
                                  'hs': str(self.page * 100),
                                  'serviceType': 'factiva.com.ui.services.SearchResultsService'},
                                  meta = {'Page':self.page},
                                  callback=self.parse_search)
