import pip
def install(package):
    pip.main(['install', package])
import numpy as np
import matplotlib.pyplot as plt
import math
import data_import
from Sondre import sondre_support_formulas as supp
import scipy
from scipy.optimize import curve_fit
import data_import as di
import os
import datetime as dt

os.chdir("C:/Users/Marky/Documents/GitHub/krypto2")
exchanges, time_list, prices, volumes= di.get_lists(opening_hours="n",make_totals="n")
# year, month, day, hour, minute = supp.fix_time_list(time_list)


prices_list = np.zeros(len(prices[0,:]))


for i in range(len(prices[0, :])):
    prices_list[i]=prices[0, i]


def rV(window):
    rvol=0
    teller=0
    for j in range(window,len(prices_list)):
        rvol = rvol + ((prices_list[j] - prices_list[j - window]) / prices_list[j]) ** 2
        teller=teller+1
    return np.sqrt(rvol*1440/(teller))

def func(x,a,b,c):
    return a*np.exp(-b*x)+c

def plot_rV(windows):
    rvols = np.zeros(len(windows))
    for i in range(len(windows)):
        rvols[i] = rV(windows[i])
        print(i,": ",rvols[i])
    windows=np.array(windows,dtype=float)
    rvols=np.array(rvols,dtype=float)
    popt,pcov=scipy.optimize.curve_fit(func,windows,rvols)
    print(popt)
    yEXP=func(windows,*popt)
    plt.plot(windows, rvols)
    plt.plot(windows,yEXP)
    plt.ylabel('Realised daily volatility')
    plt.xlabel('length of window (mins)')
    plt.show()
    return 0


windows=[]
for i in range(1,20):
    windows.append(i)

print(plot_rV(windows))
