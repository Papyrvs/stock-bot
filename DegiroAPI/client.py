from os import path
from getpass import getpass
from json import load
import requests

class Client:
    
    username: str
    password: str

    __LOGOUT_URL = 'https://trader.degiro.nl/trading/secure/logout'
    __LOGIN_URL = 'https://trader.degiro.nl/login/secure/login'
    __CLIENT_URL = 'https://trader.degiro.nl/pa/secure/client'


    def __init__(self):
        if not self.loginSaved():
            self.askLogin()

        else:
            credentials = self.getCredentials()
            self.username = credentials['username']
            self.password = credentials['password']
        
        self.sessionId = self.clientLogin()
        if self.sessionId != False:
            self.intAccount = self.clientInfo()
            if not self.loginSaved():
                self.askSave()
        else:
            exit('Login failed')
        
    def loginSaved(self) -> bool:
        return path.isfile('login.json')
    
    def askLogin(self):
        self.username = input('Username: ')
        self.password = getpass()

    
    def askSave(self):
        for _ in range(3):
            save = input('Do you wish to save your credentials for later use? Y/N: ').upper()
            print('Warning: The file is not going to be encrypted')
            if save == 'Y' or save == 'YES':
                self.createLoginFile()
                return
            elif save == 'N' or save == 'NO':
                return
            else:
                print('Wrong input')

    def createLoginFile(self):
        """Creates a login file and saved your credentials"""

        with open('login.json', 'w+') as r:
            r.write('{"username": "%s", "password": "%s"}' % (self.username, self.password))
    
    def getCredentials(self) -> dict:
        """Reads the login file and returns the credentials"""

        with open('login.json', 'r') as r:
            return load(r)
        

    def clientLogin(self) -> bool:
        """Log in with the given credentials"""

        with requests.Session() as r:
            parm = {
                "username": self.username,
                "password": self.password,
                "isPassCodeReset": False,
                "isRedirectToMobile": False
            }
            p = r.post(Client.__LOGIN_URL, json=parm)
            if 'sessionId' in p.json():
                sessionId = p.json()['sessionId']
                return sessionId

            else:
                exit('Login failed. Status code: %s' % p.status_code)
    
    def clientLogout(self):
        """Log out"""

        with requests.Session() as r:
            parm = {
                'intAccount': self.intAccount,
                'sessionId': self.sessionId,
            }
            p = r.post(Client.__LOGOUT_URL, json=parm)
        
    def clientInfo(self) -> int:
        """Gets the user's account number and returns it for later use"""
        
        with requests.Session() as r:
            parm = {
                'sessionId': self.sessionId
            }
            p = r.get(Client.__CLIENT_URL, params=parm)
            if any('intAccount' for x in p.json()):
                intAccount = p.json()['data']['intAccount']
                return intAccount

            else:
                print('Info status code: %s' % p.status_code)