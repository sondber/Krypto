import numpy as np
import math
from Sondre import sondre_support_formulas as supp


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

    #first iteration
    for k in range(0,minutes_in_first_period):
        if (k % window==0):
            try:
                rvol[0] += ((prices_list_minutes[k + window] - prices_list_minutes[k]) /
                            prices_list_minutes[k]) ** 2
            except IndexError:
                print("index =", k+window)
        rvol[0] = math.sqrt(rvol[0])
        time_list_rvol.append(time_series_minutes[k*mins])


    for i in range(1, n_entries):
        for j in range(0, mins - window): #needs to account for the first iteration
            if (j % window == 0):
                try:
                    rvol[i] += ((prices_list_minutes[i * mins + j + window] - prices_list_minutes[i * mins + j]) /
                            prices_list_minutes[i * mins + j]) ** 2
                except IndexError:
                    print("index =", i * mins + j + window)
        rvol[i] = math.sqrt(rvol[i])
        time_list_rvol.append(time_series_minutes[i * mins])
    if annualize == 1:
        if daily == 1:
            rvol = np.multiply(rvol, math.sqrt(365))
        else:
            rvol = np.multiply(rvol, math.sqrt(365 * 24))

    return rvol, time_list_rvol
