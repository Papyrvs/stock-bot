import requests

class Urls:
    def __init__(self, sessionId: str):
        with requests.Session() as r:
            p = r.get('https://trader.degiro.nl/login/secure/config', cookies={'JSESSIONID': sessionId})
            if p.status_code == 200 or p.status_code == 201:
                config = p.json()['data']
                self.tradingUrl = config['tradingUrl']
                self.paUrl = config['paUrl']
                self.productSearchUrl = config['productSearchUrl']
                self.productTypesUrl = config['productTypesUrl']
                self.reportingUrl = config['reportingUrl']
                self.vwdQuotecastServiceUrl = config['vwdQuotecastServiceUrl']
            else:
                print('Something went wrong')

        