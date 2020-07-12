## Degiro API
⚠️ Degiro could change their API at any moment, if something is not working, please open an issue.

*NOTE: THIS API IS **UNOFFICIAL***

The Degiro API is an API that is designed to interact with the trading platform called [Degiro](https://www.degiro.nl/). 

**The API is inspired by the Node.js API from [Pladaria](https://github.com/pladaria/degiro) Check it out!**



## API Usage

```python
from DegiroAPI import Degiro

tickers = ['NIO', 'TSLA'] 

obj = Degiro() # Creates an instance of degiro.Degiro()
obj.login()

ticker_data = obj.getTickerData(tickers) # Returns information about the inputted tickers

ticker_price = obj.getCurrentPrice(tickers) # Returns current price of the given stock/stocks

funds = obj.getCashFunds() # Returns your current cash funds

portfolio = obj.getPortfolio() # Returns detailed info about your portfolio. This function is not completely finished yet.

obj.logout()

```
If you rather prefer to use an interactive shell, you can use the degTerm command.

```python
from DegiroAPI import degTerm

degTerm()
```

It is also possible to use the `with` keyword when using Degiro. Then it automatically logs in and out without you specifying it.

```python

with Degiro() as obj:
    ...
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
