import pip
def install(package):
    pip.main(['install', package])
import numpy as np
import matplotlib.pyplot as plt
import math
import data_import
from Sondre import sondre_support_formulas as supp


import data_import as di
import os
import datetime as dt

os.chdir("C:/Users/Marky/Documents/GitHub/krypto")
#exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists()
#year, month, day, hour, minute = supp.fix_time_list(time_list)

prices = di.get_lists(data="p")


def realized_vol(prices):

    days_series=[]
    days_series.append(1)
    days=math.floor(len(prices)/(60*6.5))
    mins=int(60*6.5)

    rvol2,rvol3,rvol4,rvol5,rvol6,rvol7,rvol8,rvol9,rvol10,rvol15,rvol30,rvol60=np.zeros([12,days])

    for i in range(1,days):
        days_series.append(i)
        for j in range(mins):
            if (j%3==0):
                rvol3[i]=rvol3[i]+((prices[i*mins+j-3]-prices[i*mins+j])/prices[i*mins+j])**2
                if (j%6==0):
                    rvol6[i] += ((prices[i * mins + j - 6] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
                    if (j%30==0):
                        rvol30[i] += ((prices[i *  mins + j - 30] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
                        if (j%60==0):
                            rvol60[i] += ((prices[i * mins + j - 60] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
            elif (j%4==0):
                rvol4[i] += ((prices[i * mins + j - 4] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
                if (j%8==0):
                    rvol8[i] += ((prices[i * mins + j - 8] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
            elif (j%5==0):
                rvol5[i] += ((prices[i * mins + j - 5] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
                if (j%10==0):
                    rvol10[i] += ((prices[i * mins + j - 10] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
            elif (j%7==0):
                rvol7[i] += ((prices[i * mins + j - 7] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
            elif (j%9==0):
                rvol9[i] += ((prices[i * mins + j - 9] - prices[i * mins + j]) / prices[i * mins + j]) ** 2
            elif (j%15==0):
                rvol15[i] += ((prices[i * mins + j - 15] - prices[i * mins + j]) / prices[i * mins + j]) ** 2

        rvol3[i] = np.square(rvol3[i])
        rvol4[i] = np.square(rvol4[i])
        rvol5[i] = np.square(rvol5[i])
        rvol6[i] = np.square(rvol6[i])
        rvol7[i] = np.square(rvol7[i])
        rvol8[i] = np.square(rvol8[i])
        rvol9[i] = np.square(rvol9[i])
        rvol10[i] = np.square(rvol10[i])
        rvol15[i] = np.square(rvol15[i])
        rvol30[i] = np.square(rvol30[i])
        rvol60[i] = np.square(rvol60[i])


    plt.plot(days_series, rvol3, label="rvol3")
    plt.plot(days_series, rvol4, label="rvol4")
    plt.plot(days_series, rvol5, label="rvol5")
    plt.plot(days_series, rvol6, label="rvol6")
    plt.plot(days_series, rvol7, label="rvol7")
    plt.plot(days_series, rvol8, label="rvol8")
    plt.plot(days_series, rvol9, label="rvol9")
    plt.plot(days_series, rvol10, label="rvol10")
    plt.plot(days_series, rvol15, label="rvol15")
    plt.plot(days_series, rvol30, label="rvol30")
    plt.plot(days_series, rvol60, label="rvol60")

    ax=plt.subplot()
    ax.set_ylim([0,0.005])
    ax.set_xlim([750,800])
    plt.legend()
    plt.show()
    return 0



realized_vol(prices)
'''
def mins_to_days(mins_list):
    year, month, day, hour, minute = supp.fix_time_list(mins_list)
    out_list = []
    for i in range(len(mins_list)):
        if hour == 13 and minute == 30
            out_list.append(mins_list[i])

'''