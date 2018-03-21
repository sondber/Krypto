import numpy as np
import data_import as di
import matplotlib.pyplot as plt
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import os
import rolls
import scipy.stats as st
import ILLIQ
import realized_volatility
import math

"""

for i in range(0, 4):
    exchange, time_listM, pricesM, volumesM = di.get_list(i)
    print("Calculating for", exchange)
    # adjust = len(time_listM) - math.floor((len(time_listM) / 60)) * 60
    adjust = 0
    # accounting for faulty data
    time_listM = time_listM[0:len(time_listM) - adjust]
    pricesM = pricesM[0:len(pricesM) - adjust]
    volumesM = volumesM[0:len(volumesM) - adjust]

    time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

    bas = rolls.rolls(pricesM, time_listM, kill_output=1)[1]

    volumesH_clean = []
    bas_clean = []
    time_listH_clean = []

    for j in range(len(time_listH)):
        if volumesH[j] != 0 and bas[j] != 0:
            time_listH_clean.append(time_listH[j])
            volumesH_clean.append(volumesH[j])
            bas_clean.append(bas[j])

    day_time, V_average, V_lower, V_upper = dis.cyclical_average(time_listH_clean, volumesH_clean)
    day_time, bas_average, bas_lower, bas_upper = dis.cyclical_average(time_listH_clean, bas_clean)
    plot.intraday(V_average, V_lower, V_upper, title=exchange+"_"+"V")
    plot.intraday(bas_average, bas_lower, bas_upper, title=exchange+"_"+"bas")


"""

korea = 1
regular = 0
cutoff = 0

if korea ==1:
    time_list_tick, price_tick, volume_tick = dis.quick_import(4)
    time_list_minute = dis.unix_to_timestamp(time_list_tick[cutoff:])
    price_tick = price_tick[cutoff:]
    volume_tick = volume_tick[cutoff:]

else:
    exch, time_list_minute, price_tick, volume_tick = di.get_list(regular)

"""
gap = 0
equal = 0
volume_checker = volume_tick[0]
volume_checker_zero = 0
price_checker = price_tick[0]
price_checker_zero = 0
last_year, last_month, last_day, last_hour, last_minute = supp.fix_time_list(time_list_minute[0], single_time_stamp=1)


for i in range(0, len(time_list_minute)):
    volume_checker += volume_tick[i]
    price_checker += price_tick[i]
    if volume_tick[i] <= 0:
        volume_checker_zero += 1
        print(volume_tick[i])
    if price_tick[i] <= 0:
        price_checker_zero += 1

    year, month, day, hour, minute = supp.fix_time_list(time_list_minute[i], single_time_stamp=1)
    if minute > 0:
        if minute != last_minute and minute != last_minute + 1:
            gap += 1
        if minute == last_minute:
            equal += 1
    else:
        if minute != last_minute and last_minute != 59:
            gap += 1
        if minute == last_minute:
            equal += 1
    last_year, last_month, last_day, last_hour, last_minute = year, month, day, hour, minute

print(price_checker, volume_checker)
print("Number of zero-price minutes:",price_checker_zero, "Number of zero-volume minutes:", volume_checker_zero)

if korea==1:
    mins_between = 2387938 #korea
    mins_between = 183963 #korea cutof
else:
    if regular == 0:
        mins_between = 3156479 #bitstamp


print("There were", gap, "gaps", equal, "equal-minutes, and", len(time_list_minute), "entries in total")
print("In other words, there are", len(time_list_minute)-equal, "unique minutes")
print("The first entry is at", time_list_minute[0])
print("The last entry is at", time_list_minute[-1])
print("The time difference constitues", mins_between, "minutes (manual entry")

if korea==1:
    print("The data set lacks", mins_between-(len(time_list_minute)-equal), "unique minutes (", round(((mins_between-(len(time_list_minute)-equal))/mins_between)*100,3), "%")
else:
    print("The data set has", volume_checker_zero, " minutes with zero volume (", round((volume_checker_zero/mins_between)*100,3), "%")

"""

new_time_list = []
new_price_list = []
new_volume_list = []

i = 0
j = 1
accu_vol = volume_tick[0]
last_price = price_tick[0]


while j < len(time_list_minute)-1:
    while time_list_minute[j] == time_list_minute[j-1]:
        accu_vol += volume_tick[j]
        last_price = price_tick[j]
        if j < len(time_list_minute)-1:
            j += 1
        else:
            break
    new_time_list.append(time_list_minute[j])
    new_volume_list.append(accu_vol)
    new_price_list.append(last_price)
    accu_vol = 0
    if j < len(time_list_minute)-1:
        j+=1
        last_price = price_tick[j]
    else:
        break

for k in range(len(new_time_list)):
    print(new_time_list[k], new_price_list[k], '{0:.2f}'.format(new_volume_list[k]))

