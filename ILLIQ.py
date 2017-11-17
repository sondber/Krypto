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
import matplotlib.pyplot as plt


def daily_Rv(time_series_minutes, prices_list_minutes):
    year, month, day, hour, minute = supp.fix_time_list(time_series_minutes)
    if hour[0] == 0:
        mins = int(1440)
    else:
        mins = int(6.5 * 60)

    days = math.floor(len(prices_list_minutes) / (mins))
    # time_list_dates=[]
    window = 15
    rvol = np.zeros(days)
    for i in range(1, days):
        # time_list_dates.append(time_series[mins*i]) #for å få ut en datoliste: time_series[0]+the number of days later?
        for j in range(0, mins - window):
            if (j % window == 0):
                rvol[i] = rvol[i] + ((prices_list_minutes[i * mins + j + window] - prices_list_minutes[i * mins + j]) /
                                     prices_list_minutes[
                                         i * mins + j + window]) ** 2
    return rvol


def abs_returns(prices):
    ret = np.zeros(len(prices))
    for i in range(len(prices) - 1):
        ret[i] = (prices[i + 1] - prices[i]) / (prices[i + 1])
        if (ret[i] < 0):
            ret[i] = ret[i] * (-1)
    return ret


def ILLIQ(prices_hour, volume_hour):
    returns = abs_returns(prices_hour)
    illiq = np.zeros(math.floor(len(returns) / 24))
    for i in range(len(illiq)):
        illiq_hour = 0
        for j in range(24):
            if (volume_hour[24 * i + j] != 0):
                illiq_hour = illiq_hour + returns[24 * i + j] / volume_hour[24 * i + j]
        illiq[i] = illiq_hour / 24
    print("Returning daily ILLIQ ")
    return illiq


def ILLIQ_nyse_day(prices_hour, volume_hour):
    returns = abs_returns(prices_hour)
    illiq = np.zeros(math.floor(len(returns) / (7)))
    for i in range(len(illiq)):
        illiq_hour = 0
        for j in range(7):
            if (volume_hour[7 * i + j] != 0):
                illiq_hour = illiq_hour + returns[7 * i + j] / volume_hour[7 * i + j]
        illiq[i] = illiq_hour / 7
    print("Returning daily ILLIQ ")
    return illiq

# SONDRE JOBBER I DENNE
def ILLIQ_nyse_hour(time_list_minutes, prices_minutes, volumes_minutes):
    year, month, day, hour, minute = supp.fix_time_list(time_list_minutes)
    returns = abs_returns(prices_minutes)
    n_minutes =len(returns)
    n_hours = math.floor(n_minutes/390*7)
    illiq_hours = np.zeros(n_hours)

    i = 0
    j = 0

    while i < n_minutes:
        if hour[i] == 14:
            illiq_temp = 0
            for k in range(30):
                count_non_zero = 0
                if volumes_minutes[i + k] != 0:
                    illiq_temp += returns[i + k]/volumes_minutes[i + k]
                    count_non_zero += 1
            if count_non_zero > 0:
                illiq_hours[j] = illiq_temp / count_non_zero
            j += 1
            i += 30
        else:
            illiq_temp = 0
            for k in range(60):
                count_non_zero = 0
                if volumes_minutes[i + k] != 0:
                    illiq_temp += returns[i + k] / volumes_minutes[i + k]
                    count_non_zero += 1
            if count_non_zero > 0:
                illiq_hours[j] = illiq_temp / count_non_zero

            j += 1
            i += 60
    print("Length of illiq_hours:", len(illiq_hours))
    return illiq_hours

"""
def ILLIQ_nyse_year(prices_day, volume_day):
    returns = abs_returns(prices_day)
    days = 261

    illiq = np.zeros(math.floor((len(returns)) / (days)) + 1)
    for i in range(len(illiq) - 1):
        illiq_day = 0
        count = 0
        for j in range(days):
            if (volume_day[days * i + j] != 0):
                count = count + 1
                illiq_day = illiq_day + returns[days * i + j] / volume_day[days * i + j]
        illiq[i] = illiq_day / count
    illiq_day = 0
    count = 0
    for k in range(108):
        if volume_day[261 * 5 + k] != 0:
            count = count + 1
            illiq_day = illiq_day + returns[261 * 5 + k] / volume_day[261 * 5 + k]
    illiq[len(illiq) - 1] = (illiq_day / count)
    print("Returning yearly ILLIQ ")
    return illiq

"""

def p_v(prices, volumes, window):
    p_v = np.zeros(len(prices))
    for i in range(window, len(prices)):
        if sum(volumes[(i - window):i]) == 0:
            p_v[i] = 0
        else:
            p_v[i] = np.average(prices[(i - window):i]) / np.average(volumes[(i - window):i])
    plt.plot(p_v)
    plt.ylabel("monthly average rolling price/volume")
    plt.xlabel("time (2012-2017)")
    plt.show()
    return p_v


def ILLIQ_nyse_window(prices_day, volume_day, window_days, remove_outliers="No"):
    returns = abs_returns(prices_day)
    days = window_days
    illiq = np.zeros(math.floor((len(returns)) / (days)))
    for i in range(len(illiq)):
        illiq_day = np.zeros(window_days)
        for j in range(window_days):
            if (volume_day[days * i + j] != 0):
                illiq_day[j] = returns[days * i + j] / volume_day[days * i + j]
                if remove_outliers != "No" and j > 0:
                    if illiq_day[j] < illiq_day[j - 1] * 0.5 or illiq_day[j] > illiq_day[j - 1] * 2:
                        illiq_day[j] = illiq_day[j - 1]
        illiq[i] = np.median(illiq_day)

    print("Returning yearly ILLIQ ")
    return illiq