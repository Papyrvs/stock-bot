## Degiro API
⚠️ Degiro could change their API at any moment, if something is not working, please open an issue.

*NOTE: THIS API IS **UNOFFICIAL***

The Degiro API is an API that is designed to interact with the trading platform called [Degiro](https://www.degiro.nl/). 

**The API is inspired by the Node.js API from [Pladaria](https://github.com/pladaria/degiro) Check it out!**



## API Usage

```python
from Degiro import degiro

tickers = ['NIO', 'TSLA'] 
<<<<<<< HEAD
stockAmount = {'NIO': 5, 'TSLA': 4} # Key is the stock, and value is the amount 
=======
stockAmount = {'NIO': 5, 'TSLA': 4} # Key is the stock, and value is the amount NOTE: DEPRECATED
>>>>>>> 4e45ea31e8bd300ddedcdf3e9aafb21c05cdee22

obj = degiro.Degiro() # Creates an instance of degiro.Degiro()

ticker_data = obj.getTickerData(tickers) # Returns information about the inputted tickers

ticker_price = obj.getCurrentPrice(tickers) # Returns current price of the given stock/stocks

funds = obj.getCashFunds() # Returns your current cash funds

portfolio = obj.getPortfolio() # Returns detailed info about your portfolio. This function is not completely finished yet.

                                   #----------------------------------#
                                   # NOTE: DOES NOT RETURN ANYTHING.  #
                                   #     IT IS ONLY A SIMULATION!     #
                                   #      WELCOME TO THE MATRIX       #
                                   #----------------------------------#

obj.testBuy(stockAmount) # Buys stocks
obj.testSell(stockAmount) # Sells stocks

```
### Todo:
- Buy/sell stocks
- ~~Support currency~~
- Create an algorithm 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Creators
- [CarixoHD](https://github.com/CarixoHD)
- [FlyingRainbowPotato](https://github.com/FlyingRainbowPotato)

## License
[MIT](https://choosealicense.com/licenses/mit/)
