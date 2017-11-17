import ILLIQ_new as ilq
import data_import as di
from Jacob import jacob_support as jacsup
import matplotlib.pyplot as plt

#"""
exchanges, time_list, prices, volumes = di.get_lists(data="all", opening_hours="y", make_totals="n")

prices = prices[0]  # exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"
volumes = volumes[0]

returns = jacsup.logreturn(prices)

print("length of prices",len(prices))
print("length of volume",len(volumes))
print("length of returns", len(returns))

time_illiq, illiq = ilq.illiq_new(time_list, returns, volumes, day_or_hour=1, kill_output=0)

print(time_illiq)
print(illiq)


#plt.plot(illiq)
#plt.show()

"""

exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists(data="all", opening_hours="n",
                                                                                make_totals="y")

prices = total_price
volumes = total_volume
returns = jacsup.logreturn(prices)

print("length of prices",len(prices))
print("length of volume",len(volumes))
print("length of returns", len(returns))

time_illiq, illiq = ilq.illiq_new(time_list, returns, volumes, day_or_hour=1, kill_output=0)


"""