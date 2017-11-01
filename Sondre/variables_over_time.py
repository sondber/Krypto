import data_import as di
import data_import_support as dis
from Jacob import jacob_support as jake_supp
import rolls
import plot
import os
os.chdir("/Users/sondre/Documents/GitHub/krypto")




exchanges, minute_time, min_prices, min_volumes = di.get_lists(opening_hours="y", make_totals="n")
hour_time, hour_prices, hour_volumes = dis.convert_to_hour(minute_time, min_prices, min_volumes)
hour_volumes = hour_volumes[0, :]
hour_returns = jake_supp.logreturn(hour_prices[0, :])
spread, spread_rel_hour, rolls_time_list_hour, count_value_error = rolls.rolls(min_prices[0, :], minute_time, calc_basis=0, kill_output=1) # 0 -> Hour

day_time, day_prices, day_volumes = dis.convert_to_day(minute_time, min_prices, min_volumes)
day_volumes = day_volumes[0, :]
day_returns = jake_supp.logreturn(day_prices[0, :])
spread, spread_rel_day, rolls_time_list_day, count_value_error = rolls.rolls(min_prices[0, :], minute_time, calc_basis=1, kill_output=1) # 1 -> Day


xlabel = "Time"
y1_label = "Bid-ask spread"
y2_label = "Returns"
title = "Spread and Returns - Hourly"
plot.sondre_two_axes(spread_rel_hour, hour_returns, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0)
title = "Spread and Returns - Daily"
plot.sondre_two_axes(spread_rel_day, day_returns, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0)
title = "Spread and Volumes - Daily"
plot.sondre_two_axes(spread_rel_day, day_volumes, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=1)

