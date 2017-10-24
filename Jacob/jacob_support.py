import math


def logreturn(price): # takes list of prices, returns equal length list of log returns
    returnlist = [0.00] * len(price)
    for i in range(1, len(price)):
        try:
            returnlist[i] = math.log(price[i]) - math.log(price[i - 1])
        except ValueError:
            returnlist[i] = 0
    return returnlist


def price_differences(price): # takes list of prices, returns equal length list of first price differences
    returnlist = [0.00] * len(price)
    for i in range(1,len(price)):
        try:
            returnlist[i] = price[i]-price[i-1]
        except ValueError:
            returnlist[i] = 0
            print("Something wrong happened when calculating price difference")
    return returnlist



