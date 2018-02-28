import high_low_spread as hilo
import data_import as di
import data_import_support as dis
import matplotlib.pyplot as plt
import os

os.chdir("/Users/Jacob/Documents/GitHub/krypto")

exchanges, time_list, hi, lo = di.get_hilo(opening_hours="y")

exchanges1, time_list1, prices, volumes = di.get_lists(data="all", opening_hours="y", make_totals="n")


# Index for 2013 minute: 101790
# Index for 2013 hour: 1827

# Index for 2014 minute: 203580
# 2014 hour: 3654
#Index for 2015 minute : 305370
# 2015 hour: 5481

"""
#Index-finder
start = 5000
end = 6000
for i in range(len(time_list[start:end])):
    print("Time: ", time_list[start+i], "Index: ", i+start)
"""
"""

#"""
"""
timestamps = time_list[305370:]
highs = hi[0][305370:]
lows = lo[0][305370:]
prices = prices[0][305370:]
"""
#"""

#"""
hour_time, hi_hour, lo_hour = dis.convert_to_hour(time_list,hi,lo,list2_basis=0)
hour_time_closing, closing_prices, closing_prices_dummy = dis.convert_to_hour(time_list1, prices, prices, list2_basis=0)

"""
#Index-finder
start = 4000
end = 6000
for i in range(len(hour_time[start:end])):
    print("Time: ", hour_time[start+i], "Index: ", i+start)
"""
#"""
timestamps = hour_time[1827:]
highs = hi_hour[0][1827:]
lows = lo_hour[0][1827:]
prices = closing_prices[0][1827:]

"""
for i in range(len(lows)):
    print(lows[i], "::", highs[i], "::", highs[i]==lows[i])
"""


print(len(highs))
print(len(lows))
print(len(timestamps))
print(len(prices))

count_hi = 0
count_low = 0
count_same = 0
count_error = 0
count_opposite = 0
count_prices = 0

for i in range(len(highs)):
    if highs[i] == 0:
        count_hi += 1
    if lows[i] == 0:
        count_low += 1
    if highs[i] == lows[i] and not (highs[i] == 0 and lows[i] == 0):
        count_same += 1
    if (highs[i] == 0 or lows[i]==0)  or highs[i] == lows[i]:
        count_error += 1
    if highs[i]<lows[i]:
        count_opposite += 1
    if prices[i] == 0:
        count_prices = 0


print("Number of zero-highs:", count_hi)
print("number of zero-lows: ", count_low)
print("Number of same:", count_same)
print("Total", count_hi+count_low+count_same)
print("Errors", count_error)
print("Opposite", count_opposite)
print("Zero-prices", count_prices)

timelist, spreads, rel_spreads = hilo.hi_lo_spread(timestamps, highs, lows, prices, hour_yesno=1)


plt.plot(rel_spreads)
plt.show()

#"""