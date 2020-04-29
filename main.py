import sys
from Degiro import Degiro



def main():
    tickers = ['USD/CHF', 'TSLA']  # INFO: If fiat - FORMAT: USD/'currency'
    # Key is the stock, and value is the amount
    stockAmount = {'NIO': 5, 'TSLA': 4}

    # NOTE: ALL RETURNS ARE DICTIONARIES

    obj = Degiro()  # Creates an instance of degiro.Degiro()

    # Gets information about the inputted tickers
    ticker_data = obj.getTickerData(tickers)
    print(ticker_data)

    # Gets current price of the given stock/stocks
    ticker_price = obj.getCurrentPrice(tickers)
    print(ticker_price)

    funds = obj.getCashFunds()  # Returns your current cash funds
    print(funds)

    portfolio = obj.getPortfolio()  # Returns detailed info about your portfolio
    print(portfolio)

    # NOTE: DOES NOT RETURN ANYTHING.
    # IT IS ONLY A SIMULATION
    for _ in range(10):

        # Buys stocks. Key is the stock it is buying, while the value is the amount
        obj.testBuy(stockAmount)

        # Sells stocks. Key is the stock it is selling, while the value is the amount
        obj.testSell(stockAmount)
        
        print("%s %s" % (obj.buyValue('NIO'), obj.totalValue('NIO')))

    # TODO:
    # - Buy/sell stocks
    # - Support currency ---- DONE

    # NOT IN USE

        # objs = {tics: stock.Stock(credentials = credentials, ticker = tics) for tics in tickers.dticker}
        # #objs[tickers[0]].buy()
        # price_check(tickers, table, objs)'''


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nBye bye')
