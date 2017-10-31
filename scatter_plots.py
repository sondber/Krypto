import numpy as np
import data_import as di
import plot
import rolls
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
from matplotlib import pyplot as plt

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
spread_abs, spread_hourly, time_list_rolls, count_value_error = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=0, kill_output=1)
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
plot.scatters(volumes_hourly, returns_hourly, show_plot=1, xtitle="Volumes hourly [BTC]", ytitle="Returns hourly", ylims=y_lims, xlims=x_lims)


# Gammelt
"""
plot.plt.figure(1)
axes = plot.plt.gca()
axes.set_xlim([0, 1000])
axes.set_ylim([-0.05, 0.05])
plot.scatters(total_volume, returns)
plot.plt.title("Returns vs. volume")
ccf = np.corrcoef(total_volume, returns)[0,1]
print("Correlation coefficient = %0.2f" % ccf)


plot.plt.figure(2)
axes = plot.plt.gca()
axes.set_xlim([0, 1000])
axes.set_ylim([0, 0.002])
plot.scatters(total_volume, rolls)
plot.plt.title("Liquidity vs. volume")
ccf = np.corrcoef(total_volume, rolls)[0,1]
print("Correlation coefficient = %0.2f" % ccf)

# Skal være en kode som itererer gjennom årene og lager scatters på liquidity
plot.plt.figure(4)
axes = plot.plt.gca()
axes.set_xlim([0, 1000])
axes.set_ylim([0, 0.002])
i = 0
for yr in range(2013, 2018):
    temp_y = []
    temp_x = []
    yearcheck = 1
    while yearcheck:
        try:
            temp_y.append(rolls[i])
            temp_x.append(total_volume[i])
        except IndexError:
            print("error")
        i = i + 1
        try:
            if year[i] == yr:
                yearcheck = 1
            else:
                yearcheck = 0
        except IndexError:
            yearcheck = 0
    print("\nYear : %i" % yr)
    ccf = np.corrcoef(temp_x, temp_y)[0,1]
    print("Correlation coefficient = %0.2f" % ccf)
    if yr == 2013:
        clr = "black"
    elif yr == 2014:
        clr = "blue"
    elif yr == 2015:
        clr = "red"
    elif yr == 2016:
        clr = "green"
    elif yr == 2017:
        clr = "purple"
    plot.scatters(temp_x, temp_y, color=clr, label=str(yr))

plot.plt.show()
"""