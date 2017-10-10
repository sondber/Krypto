import math


def logreturn(price): #takes list of prices, returns equal length list of log returns
    returnlist = [0.00]*len(price)
    for i in range(1,len(price)):
        returnlist[i]=math.log(price[i])-math.log(price[i-1])
    return(returnlist)