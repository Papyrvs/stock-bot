import requests
import lxml.html

class Ticker:

    def yahooFormat(self, tickers: list):
        if not isinstance(tickers, list):
            tickers = [tickers]

        self.dticker = tickers[:]
        # check if theres a currency inside the list
        for i, tick in enumerate(self.dticker):
            if "/" in tick:
                tickers[i] = tick.split('/')[1] + "=X"

        self.yticker = tickers
        self.yticker = [x.upper() for x in self.yticker]

    def checkPrice(self, tickers: list) -> dict:
        self.yahooFormat(tickers)
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
        prices = {}
        for index, ticker in enumerate(self.yticker):
            url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
            with requests.Session() as s:   # Starts a session
                # Grabs content from yahoo stock site
                p = s.get(url, headers=headers)
                p.encoding = 'utf-8'
                content = lxml.html.fromstring(p.content)
                # Looks for price in the HTML
                try:
                    price = content.xpath(
                        '//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')[0].text.replace(",", "")
                    prices[self.dticker[index]] = float(price)
                except:
                    print('Error getting price: Ticker \'%s\' does not exist' % ticker)

                
        return prices


        