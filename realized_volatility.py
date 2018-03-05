import numpy as np
import math
from Sondre import sondre_support_formulas as supp


def RVol(time_series_minutes, prices_list_minutes, daily=1, annualize=0):
    year, month, day, hour, minute = supp.fix_time_list(time_series_minutes)

    if daily == 1:
        mins = int(1440)
        if hour[0] != 0:
            adjust_days = 1
        else:
            adjust_days = 0
    else:  # Altså time
        mins = int(60)

    print(len(time_series_minutes))
    print(time_series_minutes[0],time_series_minutes[len(time_series_minutes) - 1])

    n_entries = int(len(prices_list_minutes) / mins) + 1
    print(n_entries)
    minutes_in_first_period = daily * (1440 - (23 - hour[0]) * 60)
    window = 15
    rvol = np.zeros(n_entries)
    time_list = []

    j = 0
    rvol[0] += ((prices_list_minutes[minutes_in_first_period] - prices_list_minutes[0]) /
                prices_list_minutes[0]) ** 2
    rvol[0] = math.sqrt(rvol[0])
    time_list.append(time_series_minutes[0])

    for i in range(1, n_entries - 1):
        for j in range(0, mins - window):
            if (j % window == 0):
                try:
                    rvol[i] += ((prices_list_minutes[i * mins + j + window] - prices_list_minutes[i * mins + j]) /
                            prices_list_minutes[i * mins + j]) ** 2
                except IndexError:
                    print("index =", i * mins + j + window)
        rvol[i] = math.sqrt(rvol[i])
        time_list.append(time_series_minutes[i * mins])
    if annualize == 1:
        if daily == 1:
            rvol = np.multiply(rvol, math.sqrt(365))
        else:
            rvol = np.multiply(rvol, math.sqrt(365 * 24))

    return rvol, time_list
