import json
import os 
import platform
import requests
import lxml.html
import sys
import getpass
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from simulation import simulate
# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from time import sleep

class _Ticker:
    def __init__(self, tickers: list):
        if not isinstance(tickers, list):
            tickers = [tickers]

        self.dticker = tickers[:]
        # check if theres a currency inside the list
        for i, tick in enumerate(self.dticker):
            if "/" in tick:
                tickers[i] = tick.split('/')[1] + "=X"

        self.yticker = tickers
        

    def checkPrice(self) -> dict:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
        prices = {}
        for index, ticker in enumerate(self.yticker):
            try:
                url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
                with requests.Session() as s:   # Starts a session
                    p = s.get(url, headers=headers)   # Grabs content from yahoo stock site
                    p.encoding = 'utf-8'
                    content = lxml.html.fromstring(p.content)
                    price = content.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')[0].text      # Looks for price in the HTML
                    prices[self.dticker[index]] = float(price)
            except:
                print('Error while getting price')
                    
        return prices
    
class _Urls:
    def __init__(self, header: dict, sessionId: dict):
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

class _Client:

    username: str
    password: str
    headers: dict
    
    LOGIN_URL = 'https://trader.degiro.nl/login/secure/login'
    CLIENT_URL = 'https://trader.degiro.nl/pa/secure/client'

    def login(self) -> dict:
        with requests.Session() as r:
            parm = {
                "username": self.username, 
                "password": self.password, 
                "isPassCodeReset": False, 
                "isRedirectToMobile": False
            }
            p = r.post(_Client.LOGIN_URL, json = parm, headers = self.headers)
            if 'sessionId' in p.json():
                self.sessionId = p.json()['sessionId']
                return self.sessionId

            else:
                print('Login failed. Status code: %s' % p.status_code)

                return False
    
    def info(self) -> int:
        with requests.Session() as r:
            parm = {
                'sessionId': self.sessionId
            }
            p = r.get(_Client.CLIENT_URL, params = parm)
            if any('intAccount' for x in p.json()):
                return p.json()['data']['intAccount']

            else:
                print('Info status code: %s' % p.status_code)

    def credentials(self) -> dict:
        with open('login.json', 'r') as r:
            return json.load(r)

class Degiro:
    
    username: str
    password: str
    

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
        }
        self.client = _Client()
        self.client.headers = self.headers

        if not self.__saved():
            self.__askLogin()
            self.__askSave()
                 
        else:
            login = self.client.credentials()
            self.client.username = self.username = login['username']
            self.client.password = self.password = login['password']
            self.sessionId = self.client.login()
        
        self.intAccount = self.client.info()
        self.urls = _Urls(self.headers, self.sessionId)

    def __saved(self) -> bool:
            return os.path.isfile('login.json')

    def __createFile(self):
        with open('login.json', 'w+') as r:
            r.write('{"username": "%s", "password": "%s"}' % (self.username, self.password))

    def __askLogin(self):
        for _ in range(3):
                self.client.username = self.username = input('Username: ')
                self.client.password = self.password = getpass.getpass()
                login = self.client.login()
                if bool(login):
                    self.sessionId = login
                    return 
                else:
                    print('Login not successful')
        sys.exit(1)

    def __askSave(self):
        for __ in range(3):
                save: str = input('Do you wish to save your credentials for later use? Y/N: ').upper()
                if save == 'Y' or save == 'YES':
                    self.__createFile()
                    return
                elif save == 'N' or save == 'NO':
                    return
                else:
                    print('Wrong input')

    def __str__(self):
        return 'Username: %s. Password: %s' % (self.username, self.password)

    # INFO GATHERING
    def __data(self, parm: dict) -> dict:
        try:
            with requests.Session() as r:
                url = '%sv5/update/%s;jsessionid=%s' % (self.urls.tradingUrl, self.intAccount, self.sessionId)
                p = r.get(url, params = parm)
        except:
            print('Data status code: %s' % p.status_code)
            print('Unable to retrieve data')
            
        return p.json()
            
        
    def getCashFunds(self) -> dict:
        parm = {
            'cashFunds': 0
        }
        data: dict = self.__data(parm)['cashFunds']['value']
        cash = dict()
        for i in data:
            for j in i['value']:
                if j['name'] == 'currencyCode': 
                    currency: str = j['value']
                if j['name'] == 'value': 
                    amount: int = j['value']    
            if amount != 0: 
                cash[currency] = amount
        
        return cash
    
    def getCurrentPrice(self, ticker) -> dict: 
        self.__tick = _Ticker(ticker)
        return self.__tick.checkPrice()
            
        
    def getPortfolio(self) -> dict:
        parm = {
            'portfolio': 0
        }
        data = self.__data(parm)
        data: dict = data['portfolio']['value']
        
        return data
    
    def getTickerData(self, ticker) -> dict:
        self.ticker = ticker
        if not isinstance(self.ticker, list):
            self.ticker: list = [ticker]

        tickerInfo, entry = dict(), dict()
        try:
            for ticker in self.ticker:
                with requests.Session() as r:
                    url = '{}v5/products/lookup'.format(self.urls.productSearchUrl)
                    parm = {
                        'searchText': ticker,
                        'intAccount': self.intAccount, 
                        'sessionId': self.sessionId, 
                        'limit': 10
                    }
                    p = r.get(url, params = parm)
                    data: dict = p.json()
                    if 'products' in data:
                        data = data['products']
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
                    else:
                        print('Ticker \'%s\' does not exist' % ticker)
    
        except:
            print('Unable to retrieve ticker data. Status code: %s' % p.status_code)
            return {}

        return tickerInfo
    
    def testBuy(self, stockAmount):
        for ticker in stockAmount:
            print('Buying \'%s\'' % ticker) 
            if self.getTickerData(ticker):
                stock = simulate.Simulate(ticker)
                stock.SimulateBuy(stockAmount[ticker])
            else:
                print('Could not buy stock \'%s\'' % ticker)
               


    def testSell(self, stockAmount):
        for ticker in stockAmount:
            print('Selling \'%s\'' % ticker) 
            if self.getTickerData(ticker):
                stock = simulate.Simulate(ticker)
                stock.SimulateSell(stockAmount[ticker])
            else:
                print('Could not sell stock \'%s\'' % ticker)
    