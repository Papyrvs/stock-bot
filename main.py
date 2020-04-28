import sys
from Degiro import *

def main():
    tickers = ['USD/CHF', 'TSLA'] # INFO: If fiat - FORMAT: USD/'currency'
    stockAmount = {'NIO': 5, 'TSLA': 4} # Key is the stock, and value is the amount

    # NOTE: ALL RETURNS ARE DICTIONARIES

    obj = Degiro() # Creates an instance of degiro.Degiro()

    ticker_data = obj.getTickerData(tickers) # Gets information about the inputted tickers
    print(ticker_data)
    
    ticker_price = obj.getCurrentPrice(tickers) # Gets current price of the given stock/stocks
    print(ticker_price)
    
    funds = obj.getCashFunds() # Returns your current cash funds
    print(funds)

    portfolio = obj.getPortfolio() # Returns detailed info about your portfolio
    print(portfolio)

    # NOTE: DOES NOT RETURN ANYTHING. 
    # IT IS ONLY A SIMULATION

    obj.testBuy(stockAmount) # Buys stocks. Key is the stock it is buying, while the value is the amount

    obj.testSell(stockAmount) # Sells stocks. Key is the stock it is selling, while the value is the amount

    # TODO:
    # - Buy/sell stocks
    # - Support currency ---- DONE

    # NOT IN USE

        # objs = {tics: stock.Stock(credentials = credentials, ticker = tics) for tics in tickers.dticker}
        # #objs[tickers[0]].buy()
        # price_check(tickers, table, objs)'''
    
    obj = degiro.Degiro() # Creates an instance of degiro.Degiro()
    print(obj.totalValue())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nBye bye')
