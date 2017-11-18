import ILLIQ as ilq
import data_import as di
from Jacob import jacob_support as jacsup
import numpy as np
import matplotlib.pyplot as plt


exchanges, time_list, prices, volumes = di.get_lists(data="all", opening_hours="y", make_totals="n")

prices = prices[0]  # exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"
volumes = volumes[0]

returns = jacsup.logreturn(prices)

print("length of prices",len(prices))
print("length of volume",len(volumes))
print("length of returns", len(returns))


time_illiq, illiq = ilq.illiq_new(time_list, returns, volumes, day_or_hour=0, kill_output=0)


illiq = np.log(illiq)
plt.plot(illiq)
plt.show()
"""
partsum = 0
value_errors= 0
a = np.zeros(10)
a[3]=0.1
a[4] = -0.1
b = np.zeros(10)
b[3] = 1
b[4] = 1

windowsize = 10
for i in range(10):
    # print("We are in the IF %d pos and %d i", pos, i)
    if  a[i] != 0:
        partsum += abs(a[i]) / b[i]
    else:
        value_errors += 1
        partsum += 0
        windowsize -= 1
illiq_test_par = partsum/windowsize

print(illiq_test_par)
print(value_errors)
#plt.plot(illiq)
#plt.show()



exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists(data="all", opening_hours="y",
                                                                                make_totals="y")

prices = total_price
volumes = total_volume
returns = jacsup.logreturn(prices)

print("length of prices",len(prices))
print("length of volume",len(volumes))
print("length of returns", len(returns))

time_illiq, illiq = ilq.illiq_new(time_list, returns, volumes, day_or_hour=0, kill_output=0)

plt.plot(illiq)
plt.show()
"""