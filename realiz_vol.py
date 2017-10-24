import pip
def install(package):
    pip.main(['install', package])
import numpy as np
import matplotlib.pyplot as plt
import math


import data_import as di
import os


os.chdir("C:/Users/Marky/Documents/GitHub/krypto")
#volumes = di.get_lists("h", data="volume")
prices = di.get_lists("m", data="prices")

def simple_returns(prices):
    ret=np.zeros(len(prices))
    for i in range(1,len(prices)):
        if (prices[i]!=0):
            ret[i]=(int(prices[i])-int(prices[i-1]))/int(prices[i])
    return ret

def realized_vol(returns,frequency="hour"):
    if (frequency=="hour"):
        realizd = np.zeros(math.ceil(len(returns) / 60))
        realizd_hour=0
        for j in range(len(realizd)):
            for i in range(60): #teller fra 0-59, så må legge til en under for å få returns 1-60
                if (len(returns)>j*60+i+1):
                    realizd_hour+=(returns[j*60+i+1])**2
            realizd[j]=math.sqrt(realizd_hour)
            realizd_hour=0
    #elif (frequency=="daily"):  #må ha inn data med timesfrekvens
       # realizd=np.zeros(math.ceil(len))

    return realizd

def plot_list(list):
    plt.plot(list)
    plt.show()
    return 0

returns=[1,2,1,2,1,2,1,2,3,-1,0,4,1,2,3,-1,3,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,
            1,2,1,2,1,2,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,
            1,2,1,2,1,2,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4]

print(simple_returns(prices))
#print(realized_vol(simple_returns(prices)))

#plot_list(realized_vol(returns))
