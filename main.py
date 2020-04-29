import sys
from Degiro import *
import random, time

def main():
    print('Degiro Bot has started')
    stockAmount = {'NIO': 5, 'TSLA': 4} # Key is the stock, and value is the amount

    # NOTE: ALL RETURNS ARE DICTIONARIES

    obj = Degiro() # Creates an instance of degiro.Degiro()
    numBought = 0
    numSold = 0

    while True:
        if random.randint(0,99) == 99:
            obj.testBuy(stockAmount)
            numBought += 1

        if random.randint(0,20) == 20 and numSold < numBought:
            obj.testSell(stockAmount)
            numSold += 1
        time.sleep(1) #If u fucking need documentation for this u don't even deserve to be on github
        





if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\nBye bye')
