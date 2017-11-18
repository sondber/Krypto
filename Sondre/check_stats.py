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
import ILLIQ_old

os.chdir("/Users/sondre/Documents/GitHub/krypto")


exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_2013(
    time_list_minutes, prices_minutes,
    volumes_minutes)


desc.stats_for_single_list(returns_days_clean, "Returns")
desc.stats_for_single_list(log_volumes_days_clean, "Volumes")
desc.stats_for_single_list(spread_days_clean, "Roll's")
desc.stats_for_single_list(log_illiq_days_clean, "Amihud")
desc.stats_for_single_list(log_volatility_days_clean, "RVol, annualized")

desc.combined_stats(spread_days_clean, log_volumes_days_clean, name1="Rolls", name2="Volumes (transformed)")
desc.combined_stats(spread_days_clean, log_volatility_days_clean, name1="Rolls", name2="Log volatility")
desc.combined_stats(spread_days_clean, returns_days_clean, name1="Rolls", name2="Returns")
desc.combined_stats(log_illiq_days_clean, spread_days_clean, name1="Log ILLIQ", name2="Rolls")
desc.combined_stats(log_illiq_days_clean, log_volumes_days_clean, name1="Log ILLIQ", name2="Volumes (transformed)")
desc.combined_stats(log_illiq_days_clean, log_volatility_days_clean, name1="Log ILLIQ", name2="Log Volatility")
desc.combined_stats(log_illiq_days_clean, returns_days_clean, name1="Log ILLIQ", name2="Returns")