import pip
def install(package):
    pip.main(['install', package])
import numpy as np
import math
import matplotlib.pyplot as pltt
from Sondre import sondre_support_formulas as supp
import scipy
from scipy.optimize import curve_fit
import data_import as di
import data_import_support as dis
import os
import datetime as dt


def daily_Rv(time_series, prices_list):
    year, month, day, hour, minute = supp.fix_time_list(time_series)
    if hour[0]==0:
        mins = int(1440)
    else:
        mins=int(6.5*60)

    days = math.floor(len(prices_list) / (mins))
    #time_list_dates=[]
    window=15
    rvol = np.zeros(days)
    for i in range(1, days):
        #time_list_dates.append(time_series[mins*i]) #for å få ut en datoliste: time_series[0]+the number of days later?
        for j in range(0, mins-window):
            if (j % window== 0):
                rvol[i] = rvol[i] + ((prices_list[i * mins + j+window] - prices_list[i * mins + j]) / prices_list[
                    i * mins + j+window]) ** 2
    return rvol


def abs_returns(prices):
    ret=np.zeros(len(prices))
    for i in range(len(prices)-1):
        ret[i]=prices[i+1]-prices[i]
        if (ret[i]<0):
            ret[i]=ret[i]*(-1)
    return ret



def ILLIQ(prices_hour, volume_hour):
    returns = abs_returns(prices_hour)
    illiq=np.zeros(math.floor(len(returns)/24))
    for i in range(len(illiq)):
        illiq_hour=0
        for j in range(24):
            if (volume_hour[24*i+j]!=0):
                illiq_hour=illiq_hour+returns[24*i+j]/volume_hour[24*i+j]
        illiq[i]=illiq_hour/24
    print("Returning daily ILLIQ ")
    return illiq


def ILLIQ_nyse_day(prices_hour, volume_hour):
    returns=abs_returns(prices_hour)
    illiq=np.zeros(math.floor(len(returns)/(7)))
    for i in range(len(illiq)):
        illiq_hour=0
        for j in range(7):
            if (volume_hour[7*i+j]!=0):
                illiq_hour=illiq_hour+returns[7*i+j]/volume_hour[7*i+j]
        illiq[i]=illiq_hour/7
    print("Returning daily ILLIQ ")
    return illiq




