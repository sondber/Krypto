import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import realized_volatility
import rolls
import ILLIQ
os.chdir("/Users/sondre/Documents/GitHub/krypto")


exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")

"""
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
    time_list_minutes, prices_minutes,
    volumes_minutes, full_week=1)
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
    plt.plot(volumes_new[i, :], label=exchanges[i], linewidth=0.5, color="black", marker="o")
    i += 1
    plt.plot(volumes_new[i, :], label=exchanges[i], linewidth=0.5, color="black", marker="d")
    i += 1
    plt.plot(volumes_new[i, :], label=exchanges[i], linewidth=0.5,  color="black", marker="*")
    i += 1
    plt.plot(volumes_new[i, :], label=exchanges[i], linewidth=0.5, color="black", marker= "+")


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
    plt.ylabel("Traded volume [BTC/month]")
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
    plt.ylabel("Price [USD/BTC]")
    plt.legend()
    location = "figures/compex/compare_exchanges_price.png"
    plt.savefig(location)


