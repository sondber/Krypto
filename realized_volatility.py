import numpy as np
import math
from Sondre import sondre_support_formulas as supp


def daily_Rvol(time_series_minutes, prices_list_minutes):
    year, month, day, hour, minute = supp.fix_time_list(time_series_minutes)
    if hour[0] == 0:
        hours_in_day = 24
        mins = int(1440)
    else:
        mins = int(6.5 * 60)
        hours_in_day = 6.5
    days = int(len(prices_list_minutes) / mins)
    window = 15
    rvol = np.zeros(days)
    time_list = []
    for i in range(1, days):
        # time_list_dates.append(time_series[mins*i]) #for å få ut en datoliste: time_series[0]+the number of days later?
        for j in range(0, mins - window):
            if (j % window == 0):
                rvol[i] = rvol[i] + ((prices_list_minutes[i * mins + j + window] - prices_list_minutes[i * mins + j]) /
                                     prices_list_minutes[
                                         i * mins + j]) ** 2
        rvol[i] = math.sqrt(rvol[i])
        time_list.append(time_series_minutes[i*mins*hours_in_day])
    return rvol, time_list
