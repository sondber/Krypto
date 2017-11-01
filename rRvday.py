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




def rV(window,prices_list):
    days = math.floor(len(prices_list) / (1440))
    mins = int(1440)
    rvol = np.zeros(days)
    for i in range(1, days):
        for j in range(window, mins):
            if (j % window == 0):
                rvol[i] = rvol[i] + ((prices_list[i * mins + j] - prices_list[i * mins + j - window]) / prices_list[
                    i * mins + j]) ** 2

    return np.sqrt(np.median(rvol))

def func(x,a,b,c):
    return a*np.exp(-b*x)+c

def plot_rV(windows):
    yr_max=5
    rvols = np.zeros(shape=(yr_max, len(windows)))
    for yr in range(yr_max):

        prices_list = np.zeros(1440*365)
        start = len(prices[0, :]) - (yr_max-yr) * 1440 * 365

        for i in range(len(prices_list)):
            prices_list[i] = prices[0, i + start]



        for i in range(len(windows)):
            rvols[yr,i] = rV(windows[i],prices_list)
        year=2017-yr_max+yr
        plt.plot(windows, rvols[yr, :],label="year: "+str(year))

    windows=np.array(windows,dtype=float)
    '''
    rvols=np.array(rvols[0,:],dtype=float)
    popt,pcov=scipy.optimize.curve_fit(func,windows,rvols)
    print(popt)
    yEXP=func(windows,*popt)
    plt.plot(windows,yEXP)
    '''
    plt.legend()
    plt.ylabel('Realised daily volatility')
    plt.xlabel('length of window (mins)')
    plt.show()
    return 0



windows=[]
for i in range(1,30):
    windows.append(i)

print(plot_rV(windows))
