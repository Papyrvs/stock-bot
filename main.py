# import sys
# import os
# sys.path.insert(0, '%s%s' % (os.path.dirname(os.path.realpath(__file__)), '/modules/'))
# from degiro import *
import sys
from modules import degiro

def main():
    tickers = ['NIO', 'TSLA'] # INFO: If fiat - FORMAT: USD/'currency'
    
    # NOTE: ALL RETURNS ARE DICTIONARIES
    
    obj = degiro.Degiro() # Creates an instance of degiro.Degiro()
    
    ticker_data = obj.getTickerData(tickers) # Gets information about the inputted tickers
    print(ticker_data)
    
    ticker_price = obj.getCurrentPrice(tickers) # Gets current price of the given stock/stocks
    print(ticker_price)
    
    funds = obj.getCashFunds() # Returns your current cash funds
    print(funds)
    
    portfolio = obj.getPortfolio() # Returns detailed info about your portfolio
    print(portfolio)
    
    
    # TODO:
    # - Buy/sell stocks
    # - Support currency




    # NOT IN USE

        # objs = {tics: stock.Stock(credentials = credentials, ticker = tics) for tics in tickers.dticker}
        # #objs[tickers[0]].buy()
        # price_check(tickers, table, objs)
        
        
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nBye bye')