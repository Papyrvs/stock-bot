from cmd import Cmd
from DegiroAPI import degiro


class StockShell(Cmd):
    d = degiro.Degiro()
    def do_login(self, line):
        StockShell.d.login()
        print(StockShell.d.__str__())
    
    def do_logout(self, line):
        if StockShell.d.logout():
            print('Logged out')
    
    def do_cash_funds(self, line):
        """cash_funds
        Get your current cash funds"""
        fund = StockShell.d.getCashFunds()
        print(fund) if fund != None else fund
            
    def do_ticker_price(self, ticker):
        """ticker_price <ticker> 
        If you want to check many tickers:

        ticker_price <ticker> <ticker> ... <ticker>
        
        Get the current prince of the given ticker(s)"""
        if ticker == "":
            print('No ticker specified. Check \'help\' for help')
        else:
            if " " in ticker:
                ticker = list(filter(None, ticker.split(" ")))

            print(StockShell.d.getCurrentPrice(ticker))

    def do_ticker_info(self, ticker):
        """ticker_info <ticker>
        If you want to check many tickers:

        ticker_info <ticker> <ticker> ... <ticker>
        
        Get the information about the given ticker(s)"""
        if ticker == "":
            print('No ticker specified. Check \'help\' for help')
        else:
            if " " in ticker:
                ticker = list(filter(None, ticker.split(" ")))

            info = StockShell.d.getTickerInfo(ticker)
            print(info) if info != None else info
    
    def do_exit(self, line):
        exit(1)

def degTerm():
    StockShell().cmdloop()