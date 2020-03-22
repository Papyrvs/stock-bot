from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import requests
import lxml.html
import password
import prettytable
import os
import platform
from tkinter import Tk

class Aksje:
    def __init__(self, credentials, ticker):
        '''
        KAN BLI BRUKT TIL POSISJONERING AV BROWSERS
        
        root = Tk()
        WIDTH = root.winfo_screenwidth()
        HEIGHT = root.winfo_screenheight()
        '''
        self.browser = webdriver.Chrome()
        self.username = credentials['username']
        self.password = credentials['password']
        self.browser.get('https://trader.degiro.nl/login/#/login')
        self.browser.set_window_size(500, 800)
        self.ticker = ticker
        wait = WebDriverWait(self.browser, 10)
        userForm = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        passwordForm = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        userForm.send_keys(self.username)
        passwordForm.send_keys(self.password)
        self.browser.find_element_by_xpath('//*[@id="loginForm"]/div[3]/button').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="appWorkspace"]/div[2]/main/div/div[3]/div/div[1]/button'))).send_keys(ticker)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/main/div/div/div/div/div[2]/div/a[1]/div[1]/span[1]'))).click()
    def buy(self):
        print("BOUGHT")


def price_check(ticker, headers, credentials, objs):
    table = prettytable.PrettyTable()
    table.field_names = ["Ticker", "Price in USD"]
    def check(ticker):
        url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}&.tsrc=fin-srch'
        with requests.Session() as s:
            p = s.get(url, headers=headers)
            p.encoding = 'utf-8'
            content = lxml.html.fromstring(p.content)
            price = float(content.xpath('//*[@id="quote-header-info"]/div[3]/div[1]/div/span[1]')[0].text)
            table.add_row([ticker, price])
            os.system("cls") if platform.system() == "Windows" else os.system("clear")

            print(table)
            return price

    try:    
        # for _ in range(10):
        while True:
            for tickers in ticker:    
                price = check(tickers)
                
                if price < 3.2:
                    objs[tickers].buy()
    except KeyboardInterrupt:
        pass
            
def main():
    credentials = {'username': "FlyingRainbowPotato", 'password': password.pw()}

    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}

    TICKER = ['TSLA']
        
    objs = {tickers: Aksje(credentials = credentials, ticker = tickers) for tickers in TICKER}

    price_check(TICKER, headers, credentials, objs)

if __name__ == "__main__":
    main()

