import pip
def install(package):
    pip.main(['install', package])
import numpy as np
import math
import data_import as di
import os

os.chdir("C:/Users/Marky/Documents/GitHub/krypto")
volumes = di.get_lists_legacy("h", data="volume")
prices = di.get_lists_legacy("h", data="prices")
#print(prices[1:100])
#print(volumes[1:100])
def abs_returns(prices):
    ret=np.zeros(len(prices))
    for i in range(1,len(prices)):
        ret[i]=prices[i]-prices[i-1]
        if (ret[i]<0):
            ret[i]=ret[i]*(-1)
    return ret



def ILLIQ(returns, volume):
    illiq=np.zeros(math.ceil(len(returns)/24))
    for i in range(len(illiq)):
        illiq_hour=0
        for j in range(24):
            if (i*24+j>len(volume)-1):
                break
            if (volume[24*i+j]!=0):
                illiq_hour=illiq_hour+returns[24*i+j]/volume[24*i+j]
        illiq[i]=illiq_hour/24
    return illiq

#returns=[1,2,1,2,1,2,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4]
#volume=[10,11,10,13,9,14,6,8,9,6,0,2,6,8,9,6,0,2,6,8,9,6,0,2,6,8,9,6,0,2,6,8,9,6,0,2,6,8,9,6,0,2,6,8,9,6,0,2,6,8,9,6,0,2,6,8,9,6,0,2]

#ILLIQ(returns,volume)
print(ILLIQ(abs_returns(prices),volumes))
print(abs_returns(prices))
print(volumes)