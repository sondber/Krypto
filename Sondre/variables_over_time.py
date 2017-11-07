import data_import as di
import data_import_support as dis
from Jacob import jacob_support as jake_supp
import rolls
import plot
import os
import numpy as np
import ILLIQ
os.chdir("/Users/sondre/Documents/GitHub/krypto")


exchanges, minute_time, min_prices, min_volumes = di.get_lists(opening_hours="y", make_totals="n")
hour_time, hour_prices, hour_volumes = dis.convert_to_hour(minute_time, min_prices, min_volumes)
hour_volumes = hour_volumes[0, :]
hour_prices = hour_prices[0,:]
hour_returns = np.multiply(jake_supp.logreturn(hour_prices), 100)  # Percentage

day_time, day_prices, day_volumes = dis.convert_to_day(minute_time, min_prices, min_volumes)
day_volumes = day_volumes[0, :]
day_prices = day_prices[0, :]
min_prices = min_prices[0, :]
min_volumes = min_volumes[0, :]

day_returns = np.multiply(jake_supp.logreturn(day_prices),100)  # Percentage
spread, spread_rel_hour, rolls_time_list_hour, count_value_error = rolls.rolls(min_prices, minute_time, calc_basis=0, kill_output=1) # 0 -> Hour
spread, spread_rel_day, rolls_time_list_day, count_value_error = rolls.rolls(min_prices, minute_time, calc_basis=1, kill_output=1) # 1 -> Day

spread_rel_day = np.multiply(spread_rel_day, 100)  # Percentage

illiq_day = ILLIQ.ILLIQ_nyse_day(hour_prices, hour_volumes)
volatility_day = np.multiply(ILLIQ.daily_Rv(minute_time, min_prices), 100) # Percentage

vol_excluding_extremes = volatility_day[0:330]
time_excl_extremes = day_time[0:330]
spread_excl_extremes = spread_rel_day[0:330]
illiq_excl_extremes = illiq_day[0:330]
np.append(vol_excluding_extremes, volatility_day[336:len(volatility_day)])
np.append(time_excl_extremes, day_time[336:len(volatility_day)])
np.append(spread_excl_extremes, spread_rel_day[336:len(volatility_day)])
np.append(illiq_excl_extremes, illiq_day[336:len(volatility_day)])


xlabel = "Time"
y1_label = "Bid-ask spread (%)"
y2_label = "Returns (%)"
title = "Spread and Returns - Daily"
plot.sondre_two_axes(spread_rel_day, day_returns, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0)
plot.plot_x_zero([0, len(day_returns)])
title = "Spread and Volumes - Daily"
y2_label = "Volumes"
plot.sondre_two_axes(spread_rel_day, day_volumes, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0)
title = "Spread and Amihud - Daily"
y2_label = "Amihud's illiquidity"
plot.sondre_two_axes(spread_rel_day, illiq_day, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0)
title = "Spread and Volatility - Daily"
y2_label = "Volatility (%)"
plot.sondre_two_axes(spread_rel_day, volatility_day, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0)
title = "Spread and Volatility - Daily (excl. extremes)"
plot.sondre_two_axes(spread_rel_day, volatility_day, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, y2lims=[0, 1.2])

plot.plt.show()
