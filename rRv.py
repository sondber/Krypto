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
exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists()
# year, month, day, hour, minute = supp.fix_time_list(time_list)

prices_list = []
prices_list.append(9)


for i in range(len(prices[0, :])):  # fryktelig mye nuller i starten så
    prices_list.append(prices[0, i])

prices_list[0] = prices_list[1]


def rV(window):
    days = math.floor(len(prices_list) / (60 * 6.5))
    mins = int(60 * 6.5)
    rvol = np.zeros(days)
    for i in range(1, days):
        for j in range(1, mins):
            if (prices_list[i * mins + j] == 0):
                break
            if (j % window == 0):
                rvol[i] = rvol[i] + ((prices_list[i * mins + j] - prices_list[i * mins + j - window]) / prices_list[
                    i * mins + j]) ** 2
    return np.average(rvol)


def plot_rV(windows):
    rvols = np.zeros(len(windows))
    for i in range(len(windows)):
        rvols[i] = rV(windows[i])
    plt.plot(windows, rvols)
    plt.show()
    return 0


windows = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25, 30, 40, 50, 60, 70, 80]
print(plot_rV(windows))
