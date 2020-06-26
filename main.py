from DegiroAPI import degTerm, Degiro

obj = Degiro()
obj.login()
print(obj.getTickerInfo('tsla'))
print(obj.getCashFunds())
print(obj.getCurrentPrice(['nio', 'tsla', 'R']))
obj.logout()




with Degiro() as obj:
    print(obj.getTickerInfo('tsla'))
    print(obj.getCashFunds())
    print(obj.getCurrentPrice(['nio', 'tsla', 'R']))