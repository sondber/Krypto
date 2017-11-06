import numpy as np
import data_import as di
import plot
import rolls
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
from matplotlib import pyplot as plt
import ILLIQ

# Opening hours only
# Bistamp only

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
time_list_daily, prices_daily, volumes_daily = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)

daily_scatters = 1
if daily_scatters == 1:
    # Getting rolls estimator
    print("Prices: ", len(prices_minutes[0, :]))
    print("Time : ", len(time_list_minutes))
    print("n days = ", len(time_list_daily))

    spread_abs, spread_daily, time_list_rolls, count_value_error = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=1, kill_output=1)
    spread_daily = np.multiply(spread_daily, 100)  # <--- Percentage

    volatility_daily = ILLIQ.daily_Rv(time_list_minutes, prices_minutes[0, :])
    volatility_daily = np.multiply(volatility_daily, 100)  # <--- Percentage

    # Extracing BitstampUSD
    returns_daily = jake_supp.logreturn(prices_daily[0, :])  # <-- bistamp only
    returns_daily = np.multiply(returns_daily, 100)  # <--- Percentage
    volumes_daily = volumes_daily[0, :]  # bitstamp only
    illiq_daily = ILLIQ.ILLIQ_nyse_day(prices_hours[0, :], volumes_hours[0, :])  # bitstamp only
    illiq_daily = np.multiply(illiq_daily, 100)  # <--- Percentage
    # --------------------

    spread_std_day = np.std(spread_daily)
    spread_mean_day = np.mean(spread_daily)
    volume_std_day = np.std(volumes_daily)
    volume_mean_day = np.mean(volumes_daily)
    returns_std_day = np.std(returns_daily)
    returns_mean_day = np.mean(returns_daily)
    illiq_std_day = np.std(illiq_daily)
    illiq_mean_day = np.mean(illiq_daily)

    # Vil her utelate dag 330-335 fordi de er helt galemathias
    vol_excluding_extremes = volatility_daily[0:330]
    np.append(vol_excluding_extremes, volatility_daily[336:len(volatility_daily)])
    volatility_std_day = np.std(vol_excluding_extremes)
    volatility_mean_day = np.mean(vol_excluding_extremes)

    plt.figure(40)
    plt.plot(vol_excluding_extremes)

    print("Inclusive: ", np.mean(volatility_daily), np.std(volatility_daily))
    print("Exclusive: ", np.mean(vol_excluding_extremes), np.std(vol_excluding_extremes))

    y_mean = spread_mean_day
    y_std = spread_std_day
    y_lims = [0, y_mean + y_std]

    fig_count = 1


    # Rolls v Returns
    plt.figure(fig_count)
    x_mean = returns_mean_day
    x_std = returns_std_day
    x_lims = [x_mean - x_std, x_mean + x_std]
    plt.title("Bid/ask spread vs. Daily returns")
    plot.scatters(returns_daily, spread_daily, show_plot=0, xtitle="Returns daily (%)", ytitle="Spread daily (%)",
                  ylims=y_lims, xlims=x_lims)

    # Preparing for regression lines  <-------------------------
    alpha = -0.5
    beta = 0.05
    plot.regression_line(x_mean, x_std, alpha, beta)
    fig_count += 1

    # Rolls v Volumes
    plt.figure(fig_count)


    x_mean = volume_mean_day
    x_std = volume_std_day
    x_lims = [0, x_mean + x_std]
    plt.title("Bid/ask spread vs. daily traded volumes")
    plot.scatters(volumes_daily, spread_daily, show_plot=0, xtitle="Volumes daily [BTC]", ytitle="Spread daily (%)",
                  ylims=y_lims, xlims=x_lims)
    fig_count += 1

    # Rolls v Volatility
    plt.figure(fig_count)

    x_mean = volatility_mean_day
    x_std = volatility_std_day
    x_lims = [0, x_mean + x_std]
    plt.title("Bid/ask spread vs. daily volatility")
    plot.scatters(volatility_daily, spread_daily, show_plot=0, xtitle="Volatility daily (%)", ytitle="Spread daily (%)",
                  ylims=y_lims, xlims=x_lims)
    fig_count += 1


    # Returns v Volumes
    plt.figure(fig_count)

    y_mean = returns_mean_day
    y_std = returns_std_day
    y_lims = [y_mean - y_std, y_mean + y_std]
    x_mean = volume_mean_day
    x_std = volume_std_day
    x_lims = [0, x_mean + x_std]
    plt.title("Daily returns vs. Daily traded volumes")
    plot.scatters(volumes_daily, returns_daily, show_plot=0, xtitle="Volumes daily [BTC]", ytitle="Returns daily (%)",
                  ylims=y_lims, xlims=x_lims)

    fig_count += 1

    # Rolls v Returns w/ volume as size
    plt.figure(fig_count)

    x_mean = returns_mean_day
    x_std = returns_std_day
    x_lims = [x_mean - x_std, x_mean + x_std]

    y_mean = spread_mean_day
    y_std = spread_std_day
    y_lims = [0, y_mean + y_std]

    plt.title("Bid/ask spread vs. Daily returns")
    plot.scatters(returns_daily, spread_daily, show_plot=0, xtitle="Returns daily (%)", ytitle="Spread daily (%)",
                  ylims=y_lims, xlims=x_lims, areas=volumes_daily, label="Bubble size = traded volume")
    fig_count += 1

    # Rolls v Amihud (ILLIQ)
    plt.figure(fig_count)

    x_mean = np.mean(illiq_daily)
    x_std = np.std(illiq_daily)
    x_lims = [0, x_mean + x_std]

    plt.title("Rolls vs. Amihud - Daily")
    plot.scatters(illiq_daily, spread_daily, show_plot=0, xtitle="Amihud daily (%)", ytitle="Spread daily (%)",
                  ylims=y_lims, xlims=x_lims)
    fig_count += 1

    # Amihud v returns
    plt.figure(fig_count)
    y_mean = illiq_mean_day
    y_std = illiq_std_day
    y_lims = [0, y_mean + y_std]
    x_mean = returns_mean_day
    x_std = returns_std_day
    x_lims = [x_mean - x_std, x_mean + x_std]
    plt.title("Amihud vs. Daily returns")
    plot.scatters(returns_daily, illiq_daily, show_plot=0, xtitle="Returns daily (%)", ytitle="Amihud daily (%)",
                  ylims=y_lims, xlims=x_lims)
    fig_count += 1

    # Amihud v Volumes
    plt.figure(fig_count)

    x_mean = volume_mean_day
    x_std = volume_std_day
    x_lims = [0, x_mean + x_std]
    plt.title("Amihud vs. daily traded volumes")
    plot.scatters(volumes_daily, illiq_daily, show_plot=0, xtitle="Volumes daily (BTC)", ytitle="Amihud daily (%)",
                  ylims=y_lims, xlims=x_lims)
    fig_count += 1

    # Amihud v Voatility
    plt.figure(fig_count)

    x_mean = volatility_mean_day
    x_std = volatility_std_day
    x_lims = [0, x_mean + x_std]
    plt.title("Amihud vs. daily volatiltiy")
    plot.scatters(volatility_daily, illiq_daily, show_plot=1, xtitle="Volatility daily (%)", ytitle="Amihud daily (%)",
                  ylims=y_lims, xlims=x_lims)
    fig_count += 1

hourly_scatters = 0
if hourly_scatters == 1:
    spread_abs_hour, spread_hourly, time_list_rolls_hourly, count_value_error = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=0, kill_output=1)
    time_list_hours, prices_hourly, volumes_hourly = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
    returns_hourly = jake_supp.logreturn(prices_hourly[0, :])
    volumes_hourly = volumes_hourly[0, :] # Kun bitstamp

    y_mean = np.mean(spread_hourly)
    y_std = np.std(spread_hourly)
    y_lims = [0, y_mean + y_std]

    fig_count = 1

    # Rolls v Returns
    plt.figure(fig_count)

    x_mean = np.mean(returns_hourly)
    x_std = np.std(returns_hourly)
    x_lims = [x_mean-x_std, x_mean + x_std]
    plt.title("Bid/ask spread vs. Hourly returns")
    plot.scatters(returns_hourly, spread_hourly, show_plot=0, xtitle="Returns hourly", ytitle="Spread hourly", ylims=y_lims, xlims=x_lims)

    fig_count += 1
    # Rolls v Volumes
    plt.figure(fig_count)

    x_mean = np.mean(volumes_hourly)
    x_std = np.std(volumes_hourly)
    x_lims = [0, x_mean + x_std]
    plt.title("Bid/ask spread vs. Hourly traded volumes")
    plot.scatters(volumes_hourly, spread_hourly, show_plot=0, xtitle="Volumes hourly [BTC]", ytitle="Spread hourly", ylims=y_lims, xlims=x_lims)

    fig_count += 1
    # Returns v Volumes
    plt.figure(fig_count)

    y_mean = np.mean(returns_hourly)
    y_std = np.std(returns_hourly)
    y_lims = [y_mean - y_std, y_mean + y_std]
    x_mean = np.mean(volumes_hourly)
    x_std = np.std(volumes_hourly)
    x_lims = [0, x_mean + x_std]
    plt.title("Hourly returns vs. Hourly traded volumes")
    plot.scatters(volumes_hourly, returns_hourly, show_plot=0, xtitle="Volumes hourly [BTC]",
                  ytitle="Returns hourly", ylims=y_lims, xlims=x_lims)

    fig_count += 1

    # Rolls v Returns w/ volume as size
    plt.figure(fig_count)

    x_mean = np.mean(returns_hourly)
    x_std = np.std(returns_hourly)
    x_lims = [x_mean - x_std, x_mean + x_std]

    y_mean = np.mean(spread_hourly)
    y_std = np.std(spread_hourly)
    y_lims = [0, y_mean + y_std]

    plt.title("Bid/ask spread vs. Daily returns")
    plot.scatters(returns_hourly, spread_hourly, show_plot=1, xtitle="Returns hourly", ytitle="Spread hourly",
                  label="Bubble size = traded volume", ylims=y_lims, xlims=x_lims, areas=volumes_hourly)