import data_import as di
import rolls

import os

os.chdir("/Users/Jacob/Documents/GitHub/krypto")
"""
#### ALL DATA  #####

exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists(data="all", opening_hours="y",
                                                                                make_totals="y")

#spread, spread_rel, time_list, count_value_error = rolls.rolls(total_price, time_list, calc_basis = 1, kill_output=0)

spread, spread_rel, time_list, count_value_error = rolls.rolls(total_price[407550:], time_list[407550:], calc_basis=1,
                                                               kill_output=0)
                                                               
"""

#### SINGLE EXCHANGES ####

exchanges, time_list, prices, volumes = di.get_lists(data="all", opening_hours="n", make_totals="n")

prices = prices[2]  # exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"
volumes = volumes[2]

# Index-finder
start = 0
end = len(prices)
for i in range(len(time_list[start:end])):
    if not prices[start + i] == 0:
        print("Time: ", time_list[start + i], "Price: ", prices[start + i], "Volume: ", volumes[start + i], "Index: ",
              i + start)
        break


# spread, spread_rel, time_list, count_value_error = rolls.rolls(prices[527040:], time_list[527040:], calc_basis=1,
#                                                               kill_output=0)


# spread, spread_rel, time_list, count_value_error = rolls.rolls(prices[2103840:], time_list[2103840:], calc_basis=1,
#                                                               kill_output=0)


# plt.plot(spread_rel)
# plt.show()
