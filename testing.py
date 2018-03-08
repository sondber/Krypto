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

file_name = "data/test_set.csv"
n_exc = 1

time_list_minutes, prices, volumes = dis.fetch_aggregate_csv(file_name, n_exc)
prices_minutes = prices[0, :]
volumes_minutes = volumes[0, :]
returns_minutes = jake_supp.logreturn(prices_minutes)

time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)


spread_abs, spread_hours, time_list_spread, count_value_error = rolls.rolls(prices_minutes, time_list_minutes, calc_basis="h", kill_output=1)
illiq_hours_time, illiq_hours = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes, hourly_or_daily="h", threshold=0)
rvol_hours, time_list_rvol = realized_volatility.RVol(time_list_minutes, prices_minutes, daily=0, annualize=1)

time_list_removed = []
time_list_hours, time_list_removed, volumes_hours, prices_hours, rvol_hours, spread_hours = supp.remove_list1_zeros_from_all_lists(time_list_hours, time_list_removed, volumes_hours, prices_hours, rvol_hours, spread_hours)

print()
print("removed: ", time_list_removed)
print()
print("Lengths:")
print("Time: ", len(time_list_hours))
print("spread: ", len(spread_hours))
print("illiq: ", len(illiq_hours))
print()


for i in range(len(time_list_hours)):
    print(i, time_list_hours[i], "   ", prices_hours[i], "   ", volumes_hours[i], "   ",rvol_hours[i], "   ",spread_hours[i], "   ", illiq_hours[i])

#for i in range(len(time_list_days)):
#    print(i, time_list_days[i], prices_days[i], volumes_days[i])
