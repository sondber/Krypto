import data_import as di
import data_import_support as dis
from Jacob import jacob_support as jake_supp
import rolls
import plot
import os
import numpy as np
import ILLIQ
import pandas
os.chdir("/Users/sondre/Documents/GitHub/krypto")


exchanges, minute_time, min_prices, min_volumes = di.get_lists(opening_hours="y", make_totals="n")
hour_time, hour_prices, hour_volumes = dis.convert_to_hour(minute_time, min_prices, min_volumes)
hour_volumes = hour_volumes[0, :]
hour_prices = hour_prices[0,:]
hour_returns = jake_supp.logreturn(hour_prices)

day_time, day_prices, day_volumes = dis.convert_to_day(minute_time, min_prices, min_volumes)
day_volumes = day_volumes[0, :]
day_prices = day_prices[0, :]
min_prices = min_prices[0, :]
min_volumes = min_volumes[0, :]

day_returns = jake_supp.logreturn(day_prices)
spread, spread_rel_hour, rolls_time_list_hour, count_value_error = rolls.rolls(min_prices, minute_time, calc_basis=0, kill_output=1) # 0 -> Hour
spread, spread_rel_day, rolls_time_list_day, count_value_error = rolls.rolls(min_prices, minute_time, calc_basis=1, kill_output=1) # 1 -> Day


illiq_day = ILLIQ.ILLIQ_nyse_day(hour_prices, hour_volumes)
volatility_day = ILLIQ.daily_Rv(minute_time, min_prices)
anlzd_volatility_day = np.multiply(volatility_day, 250**0.5)
fignum = 1
plot.plt.figure(fignum)


plot.single_time_series_plot(day_time, day_returns, "Daily return", ylims=[-0.35, 0.35], perc=1)
plot.plot_x_zero([0, len(day_time)])
fignum += 1
plot.plt.figure(fignum)
plot.single_time_series_plot(day_time, day_volumes, "Daily volumes (BTC)", perc=0)
fignum += 1
plot.plt.figure(fignum)
plot.single_time_series_plot(day_time, spread_rel_day, "Bid/ask spread", perc=1)
fignum += 1
plot.plt.figure(fignum)
plot.single_time_series_plot(day_time, illiq_day, "Amihud", perc=1, ylims=[0, 0.0003])
fignum += 1
plot.plt.figure(fignum)
plot.single_time_series_plot(day_time, anlzd_volatility_day, "Realized volatility, annualized", ylims=[0, 0.79], perc=1)


# Dual plots
dual_plots = 1
if dual_plots == 1:
    xlabel = "Time"
    y1_label = "Bid-ask spread"
    y2_label = "Returns"
    title = "Spread and Returns - Daily"
    plot.sondre_two_axes(spread_rel_day, day_returns, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, perc1=1, perc2=1)
    plot.plot_x_zero([0, len(day_returns)])
    title = "Spread and Volumes - Daily"
    y2_label = "Volumes"
    plot.sondre_two_axes(spread_rel_day, day_volumes, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, perc1=1, perc2=0)
    title = "Spread and Amihud - Daily"
    y2_label = "Amihud's illiquidity"
    plot.sondre_two_axes(spread_rel_day, illiq_day, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, perc1=1, perc2=1, y2lims=[0, 0.0003])
    title = "Spread and Volatility - Daily"
    y2_label = "Realized volatility, annualized"
    plot.sondre_two_axes(spread_rel_day, anlzd_volatility_day, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, perc1=1, perc2=1)
    title = "Spread and Volatility - Daily (excl. extremes)"
    plot.sondre_two_axes(spread_rel_day, anlzd_volatility_day, x=day_time, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, y2lims=[0, 0.79], perc1=1, perc2=1)

plot.plt.show()
