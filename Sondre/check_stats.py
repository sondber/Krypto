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

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
time_list_day, prices_day, volumes_day = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)

spread_abs, spread_daily, time_list_rolls, count_value_error = rolls.rolls(prices_minutes[0, :], time_list_minutes,
                                                                           calc_basis=1, kill_output=1)
returns_daily = jake_supp.logreturn(prices_day[0, :])
volatility_day = ILLIQ.daily_Rv(time_list_minutes, prices_minutes[0, :])
anlzd_volatility_daily = np.multiply(volatility_day, 250**0.5)
illiq_daily = ILLIQ.ILLIQ_nyse_day(prices_hours[0, :], volumes_hours[0, :])  # bitstamp only


desc.stats_for_single_list(returns_daily, "Returns")
desc.stats_for_single_list(volumes_day[0, :], "Volumes")
desc.stats_for_single_list(spread_daily, "Roll's")
desc.stats_for_single_list(illiq_daily, "Amihud")
desc.stats_for_single_list(anlzd_volatility_daily, "RVol, annualized")

desc.combined_stats(illiq_daily, spread_daily, name1="Amihud", name2="Rolls")