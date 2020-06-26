from .urls import Urls
from .client import Client
from .utils import checkDict, checkList
from .ticker import Ticker
import requests

class Degiro:

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
    username: str
    

    def __init__(self):
        self.ticker = Ticker()
        self.loggedOut = False

    def __enter__(self):
        """Logs in the user if the person uses 'with'"""

        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Logs out the user after 'with' is done"""
        
        self.logout()

    def __str__(self):
        return 'Logged in as: %s' % (self.username)

    def login(self):
        self.client = Client()
        self.sessionId, self.intAccount, self.username = self.client.sessionId, self.client.intAccount, self.client.username
        self.urls = Urls(self.sessionId)

    
    def logout(self):
        if self.checkLogin():
            self.client.clientLogout()
            self.loggedOut = True
            self.sessionId = None
        else:
            print('Log in first')

    def checkLogin(self) -> bool:
        if 'sessionId' in dir(self) and self.loggedOut != True:
            return True 
        else:
            return False
    
    def __data(self, parm: dict) -> dict:
        if self.checkLogin():
            with requests.Session() as r:
                url = '%sv5/update/%s;jsessionid=%s' % (self.urls.tradingUrl, self.intAccount, self.sessionId)
                p = r.get(url, params=parm)

                return p.json() if p.status_code == 200 or p.status_code == 201 else print('Unable to retrieve data. Status code: %s' % p.status_code)

        else:
            print('Log in first')      

    def getCashFunds(self) -> dict:
        if self.checkLogin():
            parm = {
                'cashFunds': 0
            }
            data = self.__data(parm)['cashFunds']['value']
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
        else:
            print('Log in first')     

    def getCurrentPrice(self, tickerList: list) -> dict:
        if self.checkLogin():
            return self.ticker.checkPrice(tickerList)
        else:
            print('Log in first') 

    def getTickerInfo(self, tickerList: list) -> dict:
        if self.checkLogin():
            if not checkList(tickerList):
                tickerList = [tickerList]
            tickerList = [x.upper() for x in tickerList]
            self.tickerInfo, self.entry = dict(), dict()
            for ticker in tickerList:
                with requests.Session() as r:
                    url = '%sv5/products/lookup' % self.urls.productSearchUrl
                    parm = {
                        'searchText': ticker,
                        'intAccount': self.intAccount,
                        'sessionId': self.sessionId,
                        'limit': 10,
                        'offset': 0
                    }
                    p = r.get(url, params=parm)
                    if p.status_code == 200 or p.status_code == 201:
                        data: dict = p.json()
                        if 'products' in data:
                            self.filterTickerInfo(data, ticker)
                        else:
                            print('Ticker \'%s\' does not exist' % ticker)

                    else:
                        print('Unable to retrieve ticker data. Status code: %s' %
                                p.status_code)
                        return {}
            
            return self.tickerInfo
        else:
            print('Log in first') 

            

    def filterTickerInfo(self, data, ticker):
        data = data['products']
        for i in data:
            if i['symbol'] == ticker:
                self.entry['id'] = i['id']
                self.entry['isin'] = i['isin']
                self.entry['productType'] = i['productType']
                self.entry['tradable'] = i['tradable']
                self.entry['currency'] = i['currency']
                self.entry['closePrice'] = i['closePrice']
                self.entry['closePriceDate'] = i['closePriceDate']
                self.entry['currentPrice'] = self.getCurrentPrice(ticker)[ticker]
                self.tickerInfo[i['symbol']] = self.entry.copy()