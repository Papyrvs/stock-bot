from modules import stock, password
import prettytable
import platform
from tkinter import Tk


def price_check(ticker, headers, credentials, objs):
    table = prettytable.PrettyTable()
    table.field_names = ["Ticker", "Price in USD"]

    try:
        while True:
            for tickers in ticker:
                price = check(tickers, table)

                if float(price) < 3.2:
                    objs[tickers].buy()
    except KeyboardInterrupt:
        pass

def main():
    credentials = {'username': "FlyingRainbowPotato", 'password': password.pw()}

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
    TICKER = ['TSLA']
    objs = {tickers: stock.Stock(credentials = credentials, ticker = tickers) for tickers in TICKER}

    price_check(TICKER, headers, credentials, objs)

if __name__ == "__main__":
    main()