import high_low_spread as hilo
import data_import as di
import data_import_support as dis
import matplotlib.pyplot as plt
import os

os.chdir("/Users/Jacob/Documents/GitHub/krypto")

exchanges, time_list, hi, lo = di.get_hilo(opening_hours="y")

timestamps = time_list[101790:]
highs = hi[0][101790:]
lows = lo[0][101790:]

hour_time, hi_hour, lo_hour = dis.convert_to_hour(timestamps,highs,lows,list2_basis=0)


print(len(highs))
print(len(lows))
print(len(timestamps))

count_hi = 0
count_low = 0
count_same = 0
count_error = 0
count_opposite = 0

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


print("Number of zero-highs:", count_hi)
print("number of zero-lows: ", count_low)
print("Number of same:", count_same)
print("Total", count_hi+count_low+count_same)
print("Errors", count_error)
print("Opposite", count_opposite)

timelist, spreads = hilo.hi_lo_spread(timestamps, highs, lows)

count_neg = 0
for i in range(len(spreads)):
    if spreads[i] < 0:
        count_neg += 1

print("NEgative spreads:", count_neg)