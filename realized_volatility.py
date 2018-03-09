import numpy as np
import math
from Sondre import sondre_support_formulas as supp
import time


def RVol(time_series_minutes, prices_list_minutes, daily=1, annualize=1):
    year, month, day, hour, minute = supp.fix_time_list(time_series_minutes)

    if daily == 1:
        mins = int(1440)
    else:
        mins = int(60)

    n_entries = int(len(prices_list_minutes) / mins)
    minutes_in_first_period = daily * (1440 - (hour[0] * 60))
    window = 15
    rvol = np.zeros(n_entries)
    time_list_rvol = []

    # first iteration
    for k in range(0, minutes_in_first_period):  # this only loops if minutes_in_first_period is positive
        if (k % window == 0):
            try:
                rvol[0] += ((prices_list_minutes[k + window-1] - prices_list_minutes[k]) /
                            prices_list_minutes[k]) ** 2
            except IndexError:
                print("ERROR at index =", k + window)
    rvol[0] = math.sqrt(rvol[0])
    time_list_rvol.append(time_series_minutes[0])

    # remaining iterations
    for i in range(daily * 1, n_entries):  # starts at index 1 if daily, 0 otherwise
        for j in range(0, mins):
            if (j % window == 0):
                try:
                    rvol[i] += ((prices_list_minutes[(i-daily) * mins + j + window - 1 + minutes_in_first_period] -
                                 prices_list_minutes[(i-daily) * mins + j + minutes_in_first_period]) /
                                 prices_list_minutes[(i-daily) * mins + j + minutes_in_first_period]) ** 2
                except IndexError:
                    print("index =", i * mins + j + window + minutes_in_first_period)
        rvol[i] = math.sqrt(rvol[i])
        print("i =", i)
        time_list_rvol.append(time_series_minutes[(i * mins) + minutes_in_first_period])
    if annualize == 1:
        if daily == 1:
            rvol = np.multiply(rvol, math.sqrt(365))
        else:
            rvol = np.multiply(rvol, math.sqrt(365 * 24))

    return rvol, time_list_rvol
