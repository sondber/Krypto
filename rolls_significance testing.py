import data_import as di
import rolls


#### ALL DATA  #####
"""
exchanges, time_list, prices, volumes, total_price, total_volume = di.get_lists(data="all", opening_hours="y",
                                                                                make_totals="y")

spread, spread_rel, time_list, count_value_error = rolls.rolls(total_price, time_list, calc_basis = 1, kill_output=0)

#spread, spread_rel, time_list, count_value_error = rolls.rolls(total_price[407550:], time_list[407550:], calc_basis=1,
#                                                               kill_output=0)
                                                               
"""

#### SINGLE EXCHANGES ####
#"""
exchanges, time_list, prices, volumes = di.get_lists(data="all", opening_hours="y", make_totals="n")

prices = prices[0] # exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"


# spread, spread_rel, time_list, count_value_error = rolls.rolls(prices, time_list, calc_basis=1,
#                                                               kill_output=0)


spread, spread_rel, time_list, count_value_error = rolls.rolls(prices[407550:], time_list[407550:], calc_basis=1,
                                                                kill_output=0)

#"""
# plt.plot(spread_rel)
# plt.show()
