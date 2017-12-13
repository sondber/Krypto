import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp
import descriptive_stats as desc
import data_import_support as dis
import os
from matplotlib import pyplot as plt
import rolls
import ILLIQ
import realized_volatility

os.chdir("/Users/sondre/Documents/GitHub/krypto")


#RAW
raw = 0
combined = 0

if raw == 1:
    exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")
else:
    exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")

time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
returns_minutes = jake_supp.logreturn(prices_minutes[0, :])
returns_days = jake_supp.logreturn(prices_days[0, :])
spread_days = rolls.rolls(prices_minutes[0, :], time_list_minutes, calc_basis=1, kill_output=1)[1]
illiq_days_time, illiq_days = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes[0, :], day_or_hour=1)
# Realized volatility
volatility_days, rVol_time = realized_volatility.daily_Rvol(time_list_minutes, prices_minutes[0, :])
# Annualize the volatility
volatility_days = np.multiply(volatility_days, 252 ** 0.5)

if raw == 0:
    #CLEAN
    time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
    illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
        time_list_minutes, prices_minutes,
        volumes_minutes)


print()
if raw == 1:
    #RAW
    print("RAW------------------------------------------")
    print("Number of entries in RAW:", len(returns_days))
    desc.stats_for_single_list(volumes_days[0, :], "Volumes RAW")
    desc.stats_for_single_list(returns_days, "Returns RAW")
    desc.stats_for_single_list(volatility_days, "RVol, annualized RAW")
    desc.stats_for_single_list(spread_days, "Roll's RAW")
    desc.stats_for_single_list(illiq_days, "ILLIQ RAW")
    print("RAW END--------------------------------------")
else:
    #CLEAN
    desc.stats_for_single_list(volumes_days_clean, "Volumes")
    desc.stats_for_single_list(returns_days_clean, "Returns")
    desc.stats_for_single_list(volatility_days_clean, "RVol, annualized")
    desc.stats_for_single_list(spread_days_clean, "Roll's")
    desc.stats_for_single_list(illiq_days_clean, "ILLIQ")

    desc.stats_for_single_list(log_volumes_days_clean, "Log Volumes")
    desc.stats_for_single_list(log_illiq_days_clean, "Log ILLIQ")
    desc.stats_for_single_list(log_volatility_days_clean, "RVol, annualized")

if combined == 1:
    desc.combined_stats(spread_days_clean, log_volumes_days_clean, name1="Rolls", name2="Volumes (transformed)")
    desc.combined_stats(spread_days_clean, log_volatility_days_clean, name1="Rolls", name2="Log volatility")
    desc.combined_stats(spread_days_clean, returns_days_clean, name1="Rolls", name2="Returns")
    desc.combined_stats(log_illiq_days_clean, spread_days_clean, name1="Log ILLIQ", name2="Rolls")
    desc.combined_stats(log_illiq_days_clean, log_volumes_days_clean, name1="Log ILLIQ", name2="Volumes (transformed)")
    desc.combined_stats(log_illiq_days_clean, log_volatility_days_clean, name1="Log ILLIQ", name2="Log Volatility")
    desc.combined_stats(log_illiq_days_clean, returns_days_clean, name1="Log ILLIQ", name2="Returns")