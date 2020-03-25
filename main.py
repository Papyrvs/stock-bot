from modules import stock, password, tick
import prettytable

def price_check(tickers, table, obj):
    try:
        while True:
            price = tickers.check(table) 
            for key, value in price.items():
                if float(value) < 4:
                    tickers.buy(key, obj)

    except KeyboardInterrupt:
        pass

def main():
    table = prettytable.PrettyTable()
    table.field_names = ["Ticker", "Price in USD"]
    credentials = {'username': "FlyingRainbowPotato", 'password': password.pw()}  
    tickers = tick.ticker(["USD/CHF", "TSLA"]) # INFO: If fiat - FORMAT: USD/'currency'
    objs = {tics: stock.Stock(credentials = credentials, ticker = tics) for tics in tickers.dticker}
    
    #objs[tickers[0]].buy()
    price_check(tickers, table, objs)

if __name__ == "__main__":
    main()
