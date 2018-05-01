import numpy as np
import data_import as di
import plot
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import rolls

exchanges = [3, 4]  # select pair


remove_extremes = 1
remove_zero_volume = 1
remove_zero_bas = 1
print_cyclical = 1
print_results = 0
sum_volumes = 1

if sum_volumes==1:
    summed_volume = []
    bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(0)
    coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(3)
    kraken, time_list_krakenM, prices_krakenM, volumes_krakenM = di.get_list(5)

    bitstamp_hour_list, prices, volumes_bitstampH = dis.convert_to_hour(time_list_bitstampM, prices_bitstampM, volumes_bitstampM)
    coinbase_hour_list, prices, volumes_coinbaseH = dis.convert_to_hour(time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM)
    kraken_hour_list, prices, volumes_krakenH = dis.convert_to_hour(time_list_krakenM, prices_krakenM, volumes_krakenM)

    j = 0 #coinbase counter
    t = 0 #kraken counter
    partsum = 0

    for i in range(len(bitstamp_hour_list)):
        partsum = volumes_bitstampH[i]
        if not supp.A_before_B(bitstamp_hour_list[i], kraken_hour_list[t]) and t < len(kraken_hour_list)-1:
            if bitstamp_hour_list[i] == kraken_hour_list[t]:
                partsum += volumes_krakenH[t]
                t += 1
        if not supp.A_before_B(bitstamp_hour_list[i], coinbase_hour_list[j]) and j < len(coinbase_hour_list)-1:
            if bitstamp_hour_list[i] == coinbase_hour_list[j]:
                partsum += volumes_coinbaseH[j]
                j += 1
        summed_volume.append(partsum)

exchange_names = []

exc1 = exchanges[0]
exc_name1, time_list1M, prices1M, volumes_1M = di.get_list(exc1)
s_abs, spread_1H, spread_time_1, errs = rolls.rolls(prices1M, time_list1M, kill_output=1)
exc1_hour_list, prices, volumes_1H = dis.convert_to_hour(time_list1M, prices1M, volumes_1M)
exchange_names.append(exc_name1)

exc2 = exchanges[1]
exc_name2, time_list2M, prices2M, volumes_2M = di.get_list(exc2)
s_abs, spread_2H, spread_time_2, errs = rolls.rolls(prices2M, time_list2M, kill_output=1)
exc2_hour_list, prices, volumes_2H = dis.convert_to_hour(time_list2M, prices2M, volumes_2M)
exchange_names.append(exc_name2)

if len(exchanges) > 2:
    exc3 = exchanges[2]
    exc_name3, time_list3M, prices3M, volumes_3M = di.get_list(exc3)
    s_abs, spread_3H, spread_time_3, errs = rolls.rolls(prices3M, time_list3M, kill_output=1)
    exc3_hour_list, prices, volumes_3H = dis.convert_to_hour(time_list3M, prices3M, volumes_3M)
    exchange_names.append(exc_name3)
if len(exchanges) > 3:
    exc4 = exchanges[3]
    exc_name4, time_list4M, prices4M, volumes_4M = di.get_list(exc4)
    s_abs, spread_4H, spread_time_4, errs = rolls.rolls(prices4M, time_list4M, kill_output=1)
    exc4_hour_list, prices, volumes_4H = dis.convert_to_hour(time_list4M, prices4M, volumes_4M)
    exchange_names.append(exc_name4)
if len(exchanges) > 4:
    exc5 = exchanges[4]
    exc_name5, time_list5M, prices5M, volumes_5M = di.get_list(exc5)
    s_abs, spread_5H, spread_time_5, errs = rolls.rolls(prices5M, time_list5M, kill_output=1)
    exc5_hour_list, prices, volumes_5H = dis.convert_to_hour(time_list5M, prices5M, volumes_5M)
    exchange_names.append(exc_name5)
if len(exchanges) > 5:
    exc6 = exchanges[5]
    exc_name6, time_list6M, prices6M, volumes_6M = di.get_list(exc6)
    s_abs, spread_6H, spread_time_6, errs = rolls.rolls(prices6M, time_list6M, kill_output=1)
    exc6_hour_list, prices, volumes_6H = dis.convert_to_hour(time_list6M, prices6M, volumes_6M)
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
print(exc_name2, "time hours:", len(spread_2H))
print(spread_time_2[0], spread_time_2[-1])

hours_to_remove_1 = []
hours_to_remove_2 = []

if remove_extremes == 1:
    hours_to_remove_1 = supp.remove_extremes(hours_to_remove_1, volumes_1H, 6000)
    hours_to_remove_1 = supp.remove_extremes(hours_to_remove_1, spread_1H, 0.01)

    #hours_to_remove_2 = supp.remove_extremes(hours_to_remove_2, volumes_2H, 6000)
    hours_to_remove_2 = supp.remove_extremes(hours_to_remove_2, spread_2H, 0.01)

    spread_time_1 = np.delete(spread_time_1, hours_to_remove_1)
    spread_time_2 = np.delete(spread_time_2, hours_to_remove_2)

    volumes_2H = np.delete(volumes_2H, hours_to_remove_2)
    volumes_1H = np.delete(volumes_1H, hours_to_remove_1)

    spread_1H = np.delete(spread_1H, hours_to_remove_1)
    spread_2H = np.delete(spread_2H, hours_to_remove_2)

    print("Removed due to extremes:", len(hours_to_remove_1), len(hours_to_remove_2))

if remove_zero_volume == 1:
    hours_to_remove_1 = []
    hours_to_remove_2 = []
    for i in range(len(spread_time_1)):
        if volumes_1H[i] == 0:
            hours_to_remove_1.append(i)
    for j in range(len(spread_time_2)):
        if volumes_2H[j] == 0:
            hours_to_remove_2.append(j)

    spread_time_1 = np.delete(spread_time_1, hours_to_remove_1)
    spread_time_2 = np.delete(spread_time_2, hours_to_remove_2)

    volumes_2H = np.delete(volumes_2H, hours_to_remove_2)
    volumes_1H = np.delete(volumes_1H, hours_to_remove_1)

    spread_1H = np.delete(spread_1H, hours_to_remove_1)
    spread_2H = np.delete(spread_2H, hours_to_remove_2)

    print("Removed due to zero volume:", len(hours_to_remove_1), len(hours_to_remove_2))

if remove_zero_bas == 1:
    hours_to_remove_1 = []
    hours_to_remove_2 = []
    for i in range(len(spread_time_1)):
        if spread_1H[i] == 0:
            hours_to_remove_1.append(i)
    for j in range(len(spread_time_2)):
        if spread_2H[j] == 0:
            hours_to_remove_2.append(j)

    spread_time_1 = np.delete(spread_time_1, hours_to_remove_1)
    spread_time_2 = np.delete(spread_time_2, hours_to_remove_2)

    volumes_2H = np.delete(volumes_2H, hours_to_remove_2)
    volumes_1H = np.delete(volumes_1H, hours_to_remove_1)

    spread_1H = np.delete(spread_1H, hours_to_remove_1)
    spread_2H = np.delete(spread_2H, hours_to_remove_2)

    print("Removed due to zero bas:", len(hours_to_remove_1), len(hours_to_remove_2))

time_list_master = []
data_master = []

n1 = len(spread_time_1)
n2 = len(spread_time_2)

if n1 > n2:
    spread_time_longest = spread_time_1
    spread_time_shortest = spread_time_2
    volume_shortestH = volumes_2H
    volume_longestH = volumes_1H
    n = n1
    n_shortest = n2
    spread_longestH = spread_1H
    spread_shortestH = spread_2H
    longest_name = exc_name1
    shortest_name = exc_name2
else:
    spread_time_longest = spread_time_2
    spread_time_shortest = spread_time_1
    volume_shortestH = volumes_1H
    volume_longestH = volumes_2H
    n = n2
    n_shortest = n1
    spread_longestH = spread_2H
    spread_shortestH = spread_1H
    longest_name = exc_name2
    shortest_name = exc_name1

print("The longest set is", longest_name, ", while the shortest set is", shortest_name, "(after removal of extr and zeros))")

prev_j = 0
j = 0
print()
print("Searching......")
for i in range(0, n):
    if j == n_shortest - 1:
        break
    time_stamp = spread_time_longest[i]
    if not supp.A_before_B(time_stamp, spread_time_shortest[0]):
        prev_j = j
        while spread_time_shortest[j] != time_stamp and j < n_shortest-1:
            j += 1
        if spread_time_shortest[j] == time_stamp:
            spread_row = [spread_longestH[i], spread_shortestH[j], volume_longestH[i], volume_shortestH[j]]
            spread_row = np.matrix(spread_row)
            if len(data_master) == 0:
                data_master = spread_row
            else:
                data_master = np.append(data_master, spread_row, axis=0)
            time_list_master.append(time_stamp)
        else:
            j = prev_j


print("Finished searching.")
print("Results:")
print(time_list_master[0])
print(time_list_master[-1])
print("The length of the set is", len(time_list_master))

if print_cyclical == 1:
    day_time1, bas_average1, bas_lower1, bas_upper1 = dis.cyclical_average_legacy(time_list_master, data_master[:, 0])
    day_time2, bas_average2, bas_lower2, bas_upper2 = dis.cyclical_average_legacy(time_list_master, data_master[:, 1])

    day_time1, vol_average1, vol_lower1, vol_upper1 = dis.cyclical_average_legacy(time_list_master, data_master[:, 2])
    day_time2, vol_average2, vol_lower2, vol_upper2 = dis.cyclical_average_legacy(time_list_master, data_master[:, 3])

    name1 = longest_name + "_" + shortest_name + "1"
    name2 = longest_name + "_" + shortest_name + "2"
    plot.intraday(bas_average1, bas_lower1, bas_upper1, name1 + "_bas", perc=1)
    plot.intraday(bas_average2, bas_lower2, bas_upper2, name2 + "_bas", perc=1)
    plot.intraday(vol_average1, vol_lower1, vol_upper1, name1 + "_vol")
    plot.intraday(vol_average2, vol_lower2, vol_upper2, name2 + "_vol")

    if sum_volumes == 1:
        day_time_summed, vol_sum_ave, vol_sum_lower, vol_sum_upper = dis.cyclical_average_legacy(bitstamp_hour_list, summed_volume)
        plot.intraday(vol_sum_ave, vol_sum_lower, vol_sum_upper, "summed_volume_western")


#TESTING
if print_results == 1:
    for i in range(len(time_list_master)):
        print(time_list_master[i], data_master[i,:])


#print(np.corrcoef(np.transpose(data_master[:,0:2])))
spread = np.transpose(data_master[:,1])
volume = np.transpose(data_master[:,2])
#volume = summed_volume
print(np.corrcoef(spread,volume))

"""
test_index = 3
test_stamp = bitstamp_hour_list[test_index]
print("Timestamp test", test_stamp)
test_volume = summed_volume[test_index]

bitstamp_vol = volumes_bitstampH[test_index]

coinbase_vol = 0
kraken_vol = 0


for i in range(len(coinbase_hour_list)):
    if coinbase_hour_list[i] == test_stamp:
        coinbase_vol = volumes_coinbaseH[i]
        print("Timestamp coinbase:", coinbase_hour_list[i])
        break

for i in range(len(kraken_hour_list)):
    if kraken_hour_list[i] == test_stamp:
        kraken_vol = volumes_krakenH[i]
        print("Timestamp kraken:", kraken_hour_list[i])
        break


tot_vol = bitstamp_vol + coinbase_vol + kraken_vol
print("Diff:", tot_vol-test_volume)
print("Volumes:", tot_vol, test_volume)

if tot_vol == test_volume:
    print("Success")
"""
