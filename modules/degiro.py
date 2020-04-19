import json
import os 
import platform
import requests
import lxml.html
import sys
import getpass
# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from time import sleep

class _Ticker:
    def __init__(self, ticker):
        if not isinstance(ticker, list):
            ticker = ticker.split(",")

        ticks = ticker[:]
        # check if theres a currency inside the list
        for i, tick in enumerate(ticks):
            if "/" in tick:
                ticks[i] = tick.split('/')[1] + "=X"

        self.yticker = ticks

    def checkPrice(self):
        ticker = self.yticker
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
        prices = {}
        for i in ticker:
            try:
                url = f'https://finance.yahoo.com/quote/{i}?p={i}&.tsrc=fin-srch'
                with requests.Session() as s:   # Starts a session
                    p = s.get(url, headers=headers)   # Grabs content from yahoo stock site
                    p.encoding = 'utf-8'
                    content = lxml.html.fromstring(p.content)
                    price = content.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')[0].text      # Looks for price in the KHTML
                    prices[i] = price
            except:
                print('Error while getting price')
                    
        return prices
    
class _Urls:
    def __init__(self, header, sessionId):
        try:
            with requests.Session() as r:
                config = r.get('https://trader.degiro.nl/login/secure/config', headers = header, cookies = {'JSESSIONID': sessionId}).json()['data']
            
            self.tradingUrl = config['tradingUrl']
            self.paUrl = config['paUrl']
            self.productSearchUrl = config['productSearchUrl']
            self.productTypesUrl = config['productTypesUrl']
            self.reportingUrl = config['reportingUrl']
            self.vwdQuotecastServiceUrl = config['vwdQuotecastServiceUrl']
        except:
            print('Error while getting info')  


class Degiro:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
        self.username = input('Username: ')
        self.password = getpass.getpass()
        
   
        with requests.Session() as r:
            url = 'https://trader.degiro.nl/login/secure/login'
            parm = {"username": self.username, "password": self.password, "isPassCodeReset": False, "isRedirectToMobile": False}
            p = r.post(url, json = parm, headers = self.headers)
            
            try:
                self.sessionId = p.json()['sessionId']
            except KeyError:
                print('Login failed. Status code: %s' % p.status_code)
                sys.exit(1)
            
            self.cookies = r.cookies.get_dict()
            
        with requests.Session() as r:
            url = 'https://trader.degiro.nl/pa/secure/client'
            parm = {'sessionId': self.sessionId}
            p = r.get(url, params = parm)
            try:
                self.intAccount = p.json()['data']['intAccount']
            except:
                print('Info status code: %s' % p.status_code)
        
        self.urls = _Urls(self.headers, self.sessionId)
        
    def data(self, parm):
        try:
            with requests.Session() as r:
                url = '%sv5/update/%s;jsessionid=%s' % (self.urls.tradingUrl, self.intAccount, self.sessionId)
                p = r.get(url, params = parm)
        except:
            print('Data status code: %s' % p.status_code)
            print('Unable to retrieve data')
            
        return p.json()
            
        
    def getCashFunds(self):
        data = self.data({'cashFunds': 0})['cashFunds']['value']
        cash = dict()
        for i in data:
            for j in i['value']:
                if j['name'] == 'currencyCode': currency = j['value']
                if j['name'] == 'value': amount = j['value']    
            if amount != 0: cash[currency] = amount
        
        return cash
    
    def getCurrentPrice(self, ticker):
        self._tick = _Ticker(ticker)
        
        return self._tick.checkPrice()
            
        
    def getPortfolio(self):
        data = self.data({'portfolio': 0})
        data = data['portfolio']['value']
        
        return data
    
    def getTickerData(self, ticker):
        self.ticker = ticker
        tickerInfo, entry = dict(), dict()
        try:
            for ticker in self.ticker:
                with requests.Session() as r:
                    url = '{}v5/products/lookup'.format(self.urls.productSearchUrl)
                    parm = {'searchText': ticker,'intAccount': self.intAccount, 'sessionId': self.sessionId, 'limit': 10}
                    p = r.get(url, params = parm)
                    data = p.json()['products']
                    if '/' in ticker:
                        print(ticker, "is not supported right now") 
                    for i in data:
                        if i['symbol'] == ticker:        
                            entry['id'] = i['id']
                            entry['isin'] = i['isin']
                            entry['productType'] = i['productType']
                            entry['tradable'] = i['tradable']
                            entry['currency'] = i['currency']
                            entry['closePrice'] = i['closePrice']
                            entry['closePriceDate'] = i['closePriceDate']
                            entry['currentPrice'] = self.getCurrentPrice(ticker)[ticker]
                            tickerInfo[i['symbol']] = entry.copy()
            
        except:
            print('Unable to retrieve ticker data. Status code: %s' % p.status_code)
        
        return tickerInfo
    
    # def buyStock(self, ticker):            
    #     if isinstance(ticker, dict) == False:
    #         ticker = self.getTickerData(ticker)
            
    #     for i in ticker:
    #         ticId = ticker[i]['id']
    #         try: 
    #             driver = webdriver.Chrome()
    #         except:
    #             try:
    #                 from webdriver_manager.chrome import ChromeDriverManager
    #                 driver = webdriver.Chrome(ChromeDriverManager().install())
    #             except:
    #                 print("You can't use this program since you dont have Chrome Webdriver installed. \nPlease install the webdriver and add it to PATH. Link: https://chromedriver.chromium.org/downloads")
    
            
    #         driver.get('https://trader.degiro.nl/trader4/#/products/{}/overview'.format(ticId))
    #         driver.delete_all_cookies()
    #         for cookie in self.cookies:
    #             driver.add_cookie({
    #                 'name': cookie.name,
    #                 'value': cookie.value,
    #                 'path': '/',
    #                 'domain': cookie.domain
    #             })
    #             print(cookie.name,cookie.value, cookie.domain)
    #         for c in driver.get_cookies():
    #             print(c)
    
    
            
            # self.driver.get('https://trader.degiro.nl/login/#/login')
            # wait = WebDriverWait(self.driver, 10)
            # userForm = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
            # passwordForm = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
            # userForm.send_keys(self.username)
            # passwordForm.send_keys(self.password)
            # self.driver.find_element_by_xpath('//*[@id="loginForm"]/div[3]/button').click()
            # sleep(0.5)
            
            
            
    
        