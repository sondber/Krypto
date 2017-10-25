import pip
def install(package):
    pip.main(['install', package])
import numpy as np
import matplotlib.pyplot as plt
import math
import data_import as di
import os

#Uferdig**

#os.chdir("C:/Users/Marky/Documents/GitHub/krypto")
#volumes = di.get_lists("h", data="volume")
#prices = di.get_lists("h", data="prices")


returns=[1,2,1,2,1,2,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4,1,2,3,-1,0,4]


def moving_average(window,prices):
    moving=np.zeros(len(prices))
    print(len(prices))
    for i in range(window,len(prices)+1):
        moving[i-1]=np.sum(prices[(i-window):i])/window
        #moving[i]=(prices[i-window+1]+prices[i-window+2]+prices[i-window+3]+prices[i-window+4]+prices[i])/5
    return moving

print(moving_average(5,returns))

def plot_series(series1,series2):
    s=(len(series1),2)
    df=np.zeros(s)
    for i in range(len(series1)):
        df[i,0]=series1[i]
        df[i,1]=series2[i]
    plt.figure()
    df=df.cumsum()
    df.plot()
    plt.show()
    return 0

plot_series(moving_average(5,returns),moving_average(3,returns))

