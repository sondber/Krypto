import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
from matplotlib import pyplot as plt

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges = ["bitstampusd", "btceusd", "coinbaseusd", "krakenusd"]

# Importing data for all minutes of the day
exchanges, time_list, prices, volumes = di.get_lists(opening_hours="n", make_totals="n")
# Converting to hourly data
time_list, prices, volumes = dis.convert_to_hour(time_list, prices, volumes)
full_returns = jake_supp.logreturn(prices[0, :])

# Finding average for every hour of the day
full_day_time, full_day_avg_returns = dis.average_over_day(time_list, full_returns)

plt.plot(full_day_avg_returns[0:23], label="Returns")

labels = ["00:00\n20:00\n09:00", "06:00\n02:00\n15:00", "12:00\n08:00\n21:00", "18:00\n14:00\n03:00"]
plt.xticks(np.arange(0, 25, 6), labels)
plt.title("Average return over the course of a day")
plt.ylabel("Hourly logreturn")
plt.figtext(0.01, 0.068, "London")
plt.figtext(0.01, 0.036, "New York")
plt.figtext(0.01, 0.005, "Tokyo")

plt.legend()
plt.show()
