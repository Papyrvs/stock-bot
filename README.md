# Degiro Bot

Degiro Bot is a Python library that is currently in the making. It is being made by two high school students, and it will hopefully be the start of **Papyrvs**. 


## What is the goal of Degiro Bot?

The goal of Degiro Bot is to automate the buy/sell process in [Degiro](https://www.degiro.nl/) using machine learning and AI *(at least we hope to do that)*. As of now, the project is not finished. We are currently working on simulations and algorithms to test the bot, and the API.


## Degiro API
⚠️ Degiro could change their API at any moment, if something is not working, please open an issue.

*NOTE: THIS API IS **UNOFFICIAL***

The Degiro API is an API that is designed to interact with the trading platform called [Degiro](https://www.degiro.nl/). 

**The API is inspired by the Node.js API from [Pladaria](https://github.com/pladaria/degiro) Check it out!**



## API Usage

```python
from modules import degiro

tickers = ['NIO', 'TSLA'] 
stockAmount = {'NIO': 5, 'TSLA': 4} # Key is the stock, and value is the amount

obj = degiro.Degiro() # Creates an instance of degiro.Degiro()

ticker_data = obj.getTickerData(tickers) # Returns information about the inputted tickers

ticker_price = obj.getCurrentPrice(tickers) # Returns current price of the given stock/stocks

funds = obj.getCashFunds() # Returns your current cash funds

portfolio = obj.getPortfolio() # Returns detailed info about your portfolio. This function is not completely finished yet.

                                   #----------------------------------#
                                   # NOTE: DOES NOT RETURN ANYTHING.  #
                                   #     IT IS ONLY A SIMULATION      #
                                   #      WELCOME TO THE MATRIX       #
                                   #----------------------------------#

obj.testBuy(stockAmount) # Buys stocks. Key is the stock it is buying, while the value is the amount

obj.testSell(stockAmount) # Sells stocks. Key is the stock it is selling, while the value is the amount
```
### Todo:
- Buy/sell stocks
- ~~Support currency~~

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Creators
- [CarixoHD](https://github.com/CarixoHD)
- [FlyingRainbowPotato](https://github.com/FlyingRainbowPotato)

## License
[MIT](https://choosealicense.com/licenses/mit/)
