import numpy as np
import time
import data_import
import data_import as di
import data_import_support
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import realized_volatility
import rolls
import ILLIQ

# Hente inn alle 5

exchanges = [0, 3]

exchange_names = []

exc1 = exchanges[0]
exc_name1, time_list1M, prices1M, volumes_1M = di.get_list(exc1)
s_abs, spread_1H, spread_time_1, errs = rolls.rolls(prices1M, time_list1M, kill_output=1)
exchange_names.append(exc_name1)
exc2 = exchanges[1]
exc_name2, time_list2M, prices2M, volumes_2M = di.get_list(exc2)
s_abs, spread_2H, spread_time_2, errs = rolls.rolls(prices2M, time_list2M, kill_output=1)
exchange_names.append(exc_name2)
if len(exchanges)>2:
    exc3 = exchanges[2]
    exc_name3, time_list3M, prices3M, volumes_3M = di.get_list(exc3)
    s_abs, spread_3H, spread_time_3, errs = rolls.rolls(prices3M, time_list3M, kill_output=1)
    exchange_names.append(exc_name3)
if len(exchanges)>3:
    exc4 = exchanges[3]
    exc_name4, time_list4M, prices4M, volumes_4M = di.get_list(exc4)
    s_abs, spread_4H, spread_time_4, errs = rolls.rolls(prices4M, time_list4M, kill_output=1)
    exchange_names.append(exc_name4)
if len(exchanges)>4:
    exc5 = exchanges[4]
    exc_name5, time_list5M, prices5M, volumes_5M = di.get_list(exc5)
    s_abs, spread_5H, spread_time_5, errs = rolls.rolls(prices5M, time_list5M, kill_output=1)
    exchange_names.append(exc_name5)
if len(exchanges)>5:
    exc6 = exchanges[5]
    exc_name6, time_list6M, prices6M, volumes_6M = di.get_list(exc6)
    s_abs, spread_6H, spread_time_6, errs = rolls.rolls(prices6M, time_list6M, kill_output=1)
    exchange_names.append(exc_name6)


print("The following exchanges are included:")
for i in range(len(exchange_names)):
    print(exchange_names[i])

print()
print("Lengths:")
print()
print(exc_name1, "time minutes:", len(time_list1M))
print(time_list1M[0], time_list1M[-1])
print(exc_name1, "time hours:", len(spread_1H))
print(spread_time_1[0], spread_time_1[-1])
print(exc_name2, "time minutes:", len(time_list2M))
print(time_list2M[0], time_list2M[-1])
print(exc_name2,"time hours:", len(spread_2H))
print(spread_time_2[0], spread_time_2[-1])


time_list_master = []
spread_master = []

n1 = len(spread_time_1)
n2 = len(spread_time_2)

if n1>n2:
    spread_time_longest = spread_time_1
    spread_time_shortest = spread_time_2
    n = n1
    n_shortest = n2
    spread_longestH = spread_1H
    spread_shortestH = spread_2H
    longest_name = exc_name1
    shortest_name = exc_name2
else:
    spread_time_longest = spread_time_2
    spread_time_shortest = spread_time_1
    n = n2
    n_shortest = n1
    spread_longestH = spread_2H
    spread_shortestH = spread_1H
    longest_name = exc_name2
    shortest_name = exc_name1

print("The longest set is", longest_name, ", while the shortest set is", shortest_name)

prev_j = 0
print()
print("Searching......")
for i in range(0, n):
    time_stamp = spread_time_longest[i]
    j = max(0, prev_j)
    if not supp.A_before_B(time_stamp, spread_time_shortest[0]):
        while spread_time_shortest[j] != time_stamp and j < n_shortest:
            j += 1
        spread_row = [spread_longestH[i], spread_shortestH[j]]
        spread_row = np.matrix(spread_row)
        if len(spread_master) == 0:
            spread_master = spread_row
        else:
            spread_master = np.append(spread_master, spread_row, axis=0)
        time_list_master.append(time_stamp)
        prev_j = j

print("Finished searching.")


print("Results:")
for i in range(len(time_list_master)):
    print(time_list_master[i], spread_master[:,i])





