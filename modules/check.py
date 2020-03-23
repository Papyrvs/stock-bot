import os
import platform
import requests
import lxml.html


class ticker:
    def __init__(self, ticker):
        if isinstance(ticker, list):
            # check if its currency
            for i, tick in enumerate(ticker):
                if "/" in tick:
                    ticker[i] = tick.split('/')[1] + "=X"
        
        self.ticker = ticker



def check(ticker, table = None):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
    url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
    with requests.Session() as s:   # Starts a session
        p = s.get(url, headers=headers)   # Grabs content from yahoo stock site
        p.encoding = 'utf-8'
        content = lxml.html.fromstring(p.content)
        price = content.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')[0].text      # Looks for price in the KHTML

        # Shows the result in a table if its defined
        if table is not None:
            table.add_row([ticker, price])
            os.system("cls") if platform.system() == "Windows" else os.system("clear")
            print(table)

    return price