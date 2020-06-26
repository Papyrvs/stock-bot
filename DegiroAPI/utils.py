def checkDict(var) -> bool:
    if isinstance(var, dict):
        return True
    return False

def checkList(var) -> bool:
    if isinstance(var, list):
        return True
    return False

# def checkIfTickerExists(ticker):
#     try:
#         open('existing_tickers.txt', 'r')
#     except IOError:
#         open('existing_tickers.txt', 'w')
#     if ticker not in open('existing_tickers.txt', 'r').read():
#         if self.getTickerData(ticker):
#             with open('existing_tickers.txt', 'a+') as r:
#                 r.write('%s\n' % ticker)
#         else:
#             return False
#     return True