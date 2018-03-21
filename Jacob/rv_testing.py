import data_import as di
import legacy
import realized_volatility as rv
from matplotlib import pyplot as plt
import numpy as np

import os

os.chdir("/Users/Jacob/Documents/GitHub/krypto")

#### SINGLE EXCHANGES ####

exchanges, time_list, prices, volumes = legacy.get_lists_legacy(data="all", opening_hours="n", make_totals="n")

prices = prices[0]  # exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"
volumes = volumes[0]

# Objective: Check windows from 1 to 30 minutes for bitstamp b/c it is largest, for all data and 2013-2017


year_start = [527040, 1052640, 1578240, 2103840, 2630880]
year_end = [1052641, 1578241, 2103841, 2630881, 2848319]
year_label = [2013, 2014, 2015, 2016, 2017]
rv_mat_mean = []
rv_mat_median = []

for i in range(0, len(year_start)):
    mean_rvol = []
    median_rvol = []
    window_list = []
    for n in range(1, 31):
        rvol = rv.daily_Rvol(time_list[year_start[i]:year_end[i] + 1], prices[year_start[i]:year_end[i] + 1], window=n)[
            0]
        mean_rvol.append(np.mean(rvol))
        median_rvol.append(np.median(rvol))
        window_list.append(n)
        rvol = []
    rv_mat_mean.append(mean_rvol)
    rv_mat_median.append(median_rvol)


plt.figure(dpi=1000, figsize=[8,2])

m = 0
plt.plot(window_list, rv_mat_mean[m], label=year_label[m], color="black", linestyle=":")

m += 1
plt.plot(window_list, rv_mat_mean[m], label=year_label[m], color="black", linestyle="-.")
m += 1
plt.plot(window_list, rv_mat_mean[m], label=year_label[m], color="black", linestyle="--")
m += 1
plt.plot(window_list, rv_mat_mean[m], label=year_label[m], color="black", linewidth="1.2")
m += 1
plt.plot(window_list, rv_mat_mean[m], label=year_label[m], color="black", linewidth="0.8")
plt.ylim([0.01, 0.1])
plt.xlim([0, 30])
plt.ylabel("Mean daily RV")
plt.xlabel("Minutes per sampling interval")
#plt.legend()
location = "mean.png"
plt.savefig(location)

plt.figure(dpi=1000, figsize=[8,2])
m = 0
plt.plot(window_list, rv_mat_median[m], label=year_label[m], color="black", linestyle=":")
m += 1
plt.plot(window_list, rv_mat_median[m], label=year_label[m], color="black", linestyle="-.")
m += 1
plt.plot(window_list, rv_mat_median[m], label=year_label[m], color="black", linestyle="--")
m += 1
plt.plot(window_list, rv_mat_median[m], label=year_label[m], color="black", linewidth="1.2")
m += 1
plt.plot(window_list, rv_mat_median[m], label=year_label[m], color="black", linewidth="0.8")
plt.ylim([0.01, 0.08])
plt.xlim([0, 30])
plt.ylabel("Median daily RV")
#plt.legend()
location="median.png"
plt.savefig(location)
plt.show()

