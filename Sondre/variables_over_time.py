import data_import as di
import data_import_support as dis
import plot
import os

os.chdir("/Users/sondre/Documents/GitHub/krypto")
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
    illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(time_list_minutes, prices_minutes,
                                                                           volumes_minutes)

fig_count = 1
plot.plt.figure(fig_count)
plot.single_time_series_plot(time_list_days_clean, returns_days_clean, "Daily return", perc=1)
plot.plot_x_zero([0, len(time_list_days_clean)])
fig_count += 1
plot.plt.figure(fig_count)
plot.single_time_series_plot(time_list_days_clean, volumes_days_clean, "Daily volumes (BTC)", perc=0)
fig_count += 1
plot.plt.figure(fig_count)
plot.single_time_series_plot(time_list_days_clean, log_volumes_days_clean, "Daily volumes (Transformed)", perc=0)
fig_count += 1
plot.plt.figure(fig_count)
plot.single_time_series_plot(time_list_days_clean, spread_days_clean, "Bid/ask spread", perc=1)
fig_count += 1
plot.plt.figure(fig_count)
plot.single_time_series_plot(time_list_days_clean, illiq_days_clean, "ILLIQ", perc=1)
fig_count += 1
plot.plt.figure(fig_count)
plot.single_time_series_plot(time_list_days_clean, log_illiq_days_clean, "log ILLIQ", perc=0)
fig_count += 1
plot.plt.figure(fig_count)
plot.single_time_series_plot(time_list_days_clean, volatility_days_clean, "Volatility", perc=1)
fig_count += 1
plot.plt.figure(fig_count)
plot.single_time_series_plot(time_list_days_clean, log_volatility_days_clean, "Log volatility", perc=0)


# Dual plots
dual_plots = 0
if dual_plots == 1:
    xlabel = "Time"
    y1_label = "Bid-ask spread"
    y2_label = "Returns"
    title = "Spread and Returns - Daily"
    plot.sondre_two_axes(spread_days, returns_days, x=time_list_days_clean, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, perc1=1, perc2=1)
    plot.plot_x_zero([0, len(returns_days)])
    title = "Spread and Volumes - Daily"
    y2_label = "Volumes"
    plot.sondre_two_axes(spread_days, volumes_days, x=time_list_days_clean, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, perc1=1, perc2=0)
    title = "Spread and Amihud - Daily"
    y2_label = "Amihud's illiquidity"
    plot.sondre_two_axes(spread_days, illiq_days, x=time_list_days_clean, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, perc1=1, perc2=1, y2lims=[0, 0.0003])
    title = "Spread and Volatility - Daily"
    y2_label = "Realized volatility, annualized"
    plot.sondre_two_axes(spread_days, anlzd_volatility_days, x=time_list_days_clean, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, perc1=1, perc2=1)
    title = "Spread and Volatility - Daily (excl. extremes)"
    plot.sondre_two_axes(spread_days, anlzd_volatility_days, x=time_list_days_clean, x_label=xlabel, y1_label=y1_label, y2_label=y2_label, title=title, show_plot=0, y2lims=[0, 0.8], perc1=1, perc2=1)

plot.plt.show()
