import numpy as np
import math
from Sondre import sondre_support_formulas as supp


<<<<<<< HEAD
def daily_Rvol(time_series_minutes, prices_list_minutes, window=15):
=======
def RVol(time_series_minutes, prices_list_minutes, daily=1, annualize=0):
>>>>>>> master
    year, month, day, hour, minute = supp.fix_time_list(time_series_minutes)

    if daily == 1:
        mins = int(1440)
<<<<<<< HEAD
    else:
        mins = int(6.5 * 60)
    days = int(len(prices_list_minutes) / mins)
    #print("Number of days: ", days)
    print("Window: ", window)
    time_list = []
    rvol = []
    for i in range(0, days):  # blar gjennom dagene
        day = i*mins
        rvol_calc = 0
        # print("Index: ", i, "Time: ", time_series_minutes[i*mins])
        for j in range(0, mins-window, window):  # blar gjennom vinduene
                # print(time_series_minutes[i*mins+j])
                rvol_calc = rvol_calc + ((prices_list_minutes[day + j + window] - prices_list_minutes[
                    day + j]) / prices_list_minutes[day + j]) ** 2
        rvol.append(math.sqrt(rvol_calc))
        time_list.append(time_series_minutes[day])
=======
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

>>>>>>> master
    return rvol, time_list
