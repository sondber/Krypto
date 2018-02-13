import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
import high_low_spread as hilo
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import realized_volatility
import rolls
import ILLIQ
os.chdir("/Users/sondre/Documents/GitHub/krypto")


exchanges = ["bitstampusd", "coincheckjpy"]

#di.fetch_long_and_write(exchanges)
#dis.fuse_files(exchanges)


exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")
time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
#time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)

counter = 0
good = 0
for i in range(26304, len(time_list_hours)):
    if volumes_hours[1, i] == 0:
        print(i, time_list_hours[i], volumes_hours[1, i])
        counter += 1
    else:
        good += 1

print(counter)
print(100*counter/(counter+good))

"""
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_days(
    time_list_minutes, prices_minutes, volumes_minutes, full_week=1, exchange=1, days_excluded=1)
"""



"""
price_volume = 0
if price_volume == 1:
    n_labels = 5
    labels = []
    len_x = len(time_list_days)
    for i in range(0, n_labels):
        if i == n_labels - 1:
            index = len_x - 1
        else:
            index = i * (len_x / (n_labels - 1))
        index = int(index)
        labels.append(time_list_days[index][0:11])


    plt.figure(figsize=(8, 2), dpi=1000)
    plt.xticks(np.arange(0, len(time_list_days) + 1, len(time_list_days) / (n_labels - 1)), labels)
    plt.plot(prices_days[0,:], linewidth=0.5, color="black")
    ymin=0
    ymax=max(prices_days[0,:])

    plt.ylim([ymin, ymax])
    plt.xlim([0, len(time_list_days)])
    ax = plt.gca()
    vals = ax.get_yticks()
    frmt = '{:3.0f} USD'
    ax.set_yticklabels([frmt.format(x) for x in vals])

    title="price"
    location = "figures/variables_over_time/" + title + ".png"
    plt.savefig(location)

    # Volume
    plt.figure(figsize=(8, 2), dpi=1000)
    plt.xticks(np.arange(0, len(time_list_days) + 1, len(time_list_days) / (n_labels - 1)), labels)
    plt.plot(volumes_days[0,:], linewidth=0.5, color="black")
    ymin=0
    ymax=max(volumes_days[0,:])

    plt.ylim([ymin, ymax])
    plt.xlim([0, len(time_list_days)])
    ax = plt.gca()
    vals = ax.get_yticks()
    ax.set_yticklabels(["0 BTC", "50 000 BTC", "100 000 BTC"])


    title="volume"
    location = "figures/variables_over_time/" + title + ".png"
    plt.savefig(location)

"""

"""
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
    time_list_minutes, prices_minutes,
    volumes_minutes, full_week=1)
"""


"""
# Realized volatility
volatility_days, rVol_time = realized_volatility.daily_Rvol(time_list_minutes, prices_minutes[0, :])
# Annualize the volatility
volatility_days = np.multiply(volatility_days, 365 ** 0.5)

y_min = max(0.00001, min(volatility_days))
y_max = max(volatility_days)

ylims = [y_min*0.99, y_max*1.01]

plt.figure()
plt.ylim(ylims)

plt.plot(volatility_days)
plt.yscale("log", basey=np.exp(1))
labels = [y_min,y_min + 0.3*(y_max-y_min), y_min + 0.5*(y_max-y_min), y_max]
plt.yticks(labels, labels)

ax = plt.gca()
vals = ax.get_yticks()
ndigits=3
frmt = '{:3.' + str(ndigits) + 'f}%'
ax.set_yticklabels([frmt.format(x * 100) for x in vals])

plt.show()
"""


compex = 0
if compex == 1:
    time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
    # lower frequency:
    n_in = len(time_list_days)
    print(n_in)
    n_out = 63 # bimonthly
    factor = int(n_in/n_out)

    volumes_new = np.zeros([len(exchanges), n_out])
    time_list_new = []
    for i in range(0, n_out):
        for j in range(0, len(exchanges)):
            volumes_new[j, i] = np.sum(volumes_days[j, i*factor:(i+1)*factor])  # To get monthly
            if volumes_new[j, i] < 2000:
                volumes_new[j, i] = -1000000
        time_list_new.append(time_list_days[i*factor])


    plt.figure(figsize=(8, 3), dpi=1000)
    i = 0
    plt.plot(volumes_new[i, :], label=exchanges[i], linewidth=0.5, color="black", marker="+")
    i += 1
    plt.plot(volumes_new[i, :], label=exchanges[i], linewidth=0.5, color="black", marker="d")
    i += 1
    plt.plot(volumes_new[i, :], label=exchanges[i], linewidth=0.5,  color="black", marker="*")
    i += 1
    plt.plot(volumes_new[i, :], label=exchanges[i], linewidth=0.5, color="black", marker= "o")


    n_labels = 5
    labels = []
    len_x = len(time_list_days)
    for i in range(0, n_labels):
        if i == n_labels - 1:
            index = len_x - 1
        else:
            index = i * (len_x / (n_labels - 1))
        index = int(index)
        labels.append(time_list_days[index][0:11])


    plt.xticks(np.arange(0, len(time_list_new) + 1, len(time_list_new) / (n_labels - 1)), labels)
    plt.xlim([0, len(time_list_new)])
    plt.ylim([0, 1150000])

    ax = plt.gca()
    ax.set_yticklabels(["0", "200", "400", "600", "800", "1 000"])

    plt.ylabel("Volume ['000 BTC/month]")
    plt.legend()
    location = "figures/compex/compare_exchanges_volume.png"
    plt.savefig(location)




    plt.figure(figsize=(8, 3), dpi=1000)

    n_labels = 5
    labels = []
    len_x = len(time_list_days)
    for i in range(0, n_labels):
        if i == n_labels - 1:
            index = len_x - 1
        else:
            index = i * (len_x / (n_labels - 1))
        index = int(index)
        labels.append(time_list_days[index][0:11])

    plt.xticks(np.arange(0, len(time_list_days) + 1, len(time_list_days) / (n_labels - 1)), labels)
    plt.xlim([0, len(time_list_days)])
    plt.ylim([0, 2500])

    i = 0
    plt.plot(prices_days[i, :], label=exchanges[i], linewidth=0.7, color="black")
    i += 1
    plt.plot(prices_days[i, :], label=exchanges[i], linewidth=0.7, color="black", linestyle=":")
    i += 1
    plt.plot(prices_days[i, :], label=exchanges[i], linewidth=0.7,  color="black", linestyle="-.")
    i += 1
    plt.plot(prices_days[i, :], label=exchanges[i], linewidth=0.7, color="black", linestyle="--")
    ax = plt.gca()
    ax.set_yticklabels(["0", "500", "1 000", "1 500", "2 000", "2 500"])

    plt.ylabel("Price [USD/BTC]")
    plt.legend()
    location = "figures/compex/compare_exchanges_price.png"
    plt.savefig(location)


