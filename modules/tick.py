import os
import platform
import requests
import lxml.html
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from modules import stock

class ticker:
    def __init__(self, ticker):
        if not isinstance(ticker, list):
            ticker = ticker.split(",")

        ticks = ticker[:]
        # check if theres a currency inside the list
        for i, tick in enumerate(ticks):
            if "/" in tick:
                ticks[i] = tick.split('/')[1] + "=X"

        self.yticker = ticks
        self.dticker = ticker

    def check(self, table = None):
        ticker = self.yticker
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
        prices = {}
        for i in ticker:
            url = f'https://finance.yahoo.com/quote/{i}?p={i}&.tsrc=fin-srch'
            with requests.Session() as s:   # Starts a session
                p = s.get(url, headers=headers)   # Grabs content from yahoo stock site
                p.encoding = 'utf-8'
                content = lxml.html.fromstring(p.content)
                price = content.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')[0].text      # Looks for price in the KHTML
                prices[i] = price
                # Shows the result in a table if its defined
                if table is not None:
                    table.add_row([i, price])
                    os.system("cls") if platform.system() == "Windows" else os.system("clear")
                    print(table)
                
        return prices
    
    def buy(self, ticker, obj):
        index = self.yticker.index(ticker)
        obj[self.dticker[index]].buy()

            