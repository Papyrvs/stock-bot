from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
# import Tkinter

class Stock:
    def __init__(self, credentials, ticker):
        '''
        KAN BLI BRUKT TIL POSISJONERING AV BROWSERS

        root = Tk()
        WIDTH = root.winfo_screenwidth()
        HEIGHT = root.winfo_screenheight()
        '''
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
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
        print("BOUGHT " + self.ticker)



