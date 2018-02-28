import numpy as np
import math
from Sondre import sondre_support_formulas as supp


def daily_Rvol(time_series_minutes, prices_list_minutes, window=15):
    year, month, day, hour, minute = supp.fix_time_list(time_series_minutes)
    if hour[0] == 0:
        mins = int(1440)
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
    return rvol, time_list
