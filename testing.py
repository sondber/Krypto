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
intraday = 1
intraweek = 1
plots = 1
print_table = 0

time_list_minutes, prices, volumes = dis.fetch_aggregate_csv(file_name, n_exc)
y, mo, d, h, mi = supp.fix_time_list(time_list_minutes, 9)
time_list_minutes = supp.make_time_list(y, mo, d, h, mi )

prices_minutes = prices[0, :]
volumes_minutes = volumes[0, :]
returns_minutes = jake_supp.logreturn(prices_minutes)

time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)
spread_hours = rolls.rolls(prices_minutes, time_list_minutes, calc_basis="h", kill_output=1)[1]

illiq_hours_time, illiq_hours = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes, hourly_or_daily="h", threshold=0)
rvol_hours, time_list_hours_rvol = realized_volatility.RVol(time_list_minutes, prices_minutes, daily=0, annualize=1)

if intraday == 1:
    time_list_removed = []
    time_list_hours, time_list_removed, volumes_hours, prices_hours, rvol_hours, spread_hours = supp.remove_list1_zeros_from_all_lists(time_list_hours, time_list_removed, volumes_hours, prices_hours, rvol_hours, spread_hours)
    time_list_hours, time_list_removed, rvol_hours, volumes_hours, prices_hours, spread_hours, illiq_hours = supp.remove_list1_zeros_from_all_lists(time_list_hours, time_list_removed, rvol_hours, volumes_hours, prices_hours, spread_hours, illiq_hours)
    time_list_hours, time_list_removed, spread_hours, rvol_hours, volumes_hours, prices_hours, illiq_hours = supp.remove_list1_zeros_from_all_lists(time_list_hours, time_list_removed, spread_hours, rvol_hours, volumes_hours, prices_hours, illiq_hours)
    time_list_hours, time_list_removed, illiq_hours, spread_hours, rvol_hours, volumes_hours, prices_hours = supp.remove_list1_zeros_from_all_lists(time_list_hours, time_list_removed, illiq_hours, spread_hours, rvol_hours, volumes_hours, prices_hours)

    print()
    print("removed: ")
    for i in range(len(time_list_removed)):
        print(time_list_removed[i])

    print()
    print("Lengths:")
    print("Time: ", len(time_list_hours))
    print("spread: ", len(spread_hours))
    print("illiq: ", len(illiq_hours))
    print()


    log_rvol_hours = np.log(rvol_hours)
    log_illiq_hours = np.log(illiq_hours)

    if print_table == 1:
        print("    Time            Price     Volume     RVol       BAS       ILLIQ      Log-RVol    Log-ILLIQ")
        for i in range(len(time_list_hours)):
            print(time_list_hours[i], "   ", prices_hours[i], "   ", volumes_hours[i], "   ","{0:.3f}".format(rvol_hours[i]), "   ","{0:.3f}%".format(100*spread_hours[i]), "   ", "{0:.3f}%".format(100*illiq_hours[i]), "   ", "{0:.3f}".format(log_rvol_hours[i]), "   ", "{0:.3f}".format(log_illiq_hours[i]))
        print()

    hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_list_hours,
                                                                                               volumes_hours,
                                                                                               frequency="h")
    hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_list_hours,
                                                                                            spread_hours, frequency="h")
    hour_of_day, avg_rvol_hour, low_rvol_hour, upper_rvol_hour = dis.cyclical_average(time_list_hours, rvol_hours,
                                                                                      frequency="h")
    hour_of_day, avg_illiq_hour, low_illiq_hour, upper_illiq_hour = dis.cyclical_average(time_list_hours, illiq_hours,
                                                                                         frequency="h", print_n_entries=1, print_val_tab=0)

    if plots == 1:
        plt.plot(avg_volumes_hour)
        plt.title("volum")
        plt.figure()
        plt.plot(avg_spread_hour)
        plt.title("spread")
        plt.figure()
        plt.plot(avg_rvol_hour)
        plt.title("rvol")
        plt.figure()
        plt.plot(avg_illiq_hour)
        plt.title("illiq")
        plt.figure()

if intraweek == 1:
    time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
    spread_days = rolls.rolls(prices_minutes, time_list_minutes, calc_basis="d", kill_output=1)[1]
    illiq_days_time, illiq_days = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes, hourly_or_daily="d", threshold=0)
    rvol_days, time_list_days_rvol = realized_volatility.RVol(time_list_minutes, prices_minutes, daily=1, annualize=1)

    log_rvol_days = np.log(rvol_days)
    log_illiq_days = np.log(illiq_days)

    if print_table == 1:
        print("    Time            Price     Volume     RVol       BAS       ILLIQ      Log-RVol    Log-ILLIQ")
        for i in range(len(time_list_days)):
            print(time_list_days[i], "   ", prices_days[i], "   ", volumes_days[i], "   ","{0:.3f}".format(rvol_days[i]), "   ", "{0:.3f}%".format(100 * spread_days[i]), "   ","{0:.3f}%".format(100 * illiq_days[i]), "   ", "{0:.3f}".format(log_rvol_days[i]), "   ", "{0:.3f}".format(log_illiq_days[i]))
        print()

    day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.cyclical_average(time_list_days, spread_days, frequency="d")
    day_of_week, avg_volume_day, low_log_volume_day, upper_log_volume_day = dis.cyclical_average(time_list_days, volumes_days, frequency="d")
    day_of_week, avg_rvol_day, low_volatility_day_clean, upper_volatility_day_clean = dis.cyclical_average(time_list_days, rvol_days, frequency="d")
    day_of_week, avg_illiq_day, low_illiq_day_clean, upper_illiq_day_clean = dis.cyclical_average(time_list_days, illiq_days, frequency="d", print_val_tab=0)

    if plots == 1:
        plt.plot(avg_spread_day)
        plt.title("spread dag")
        plt.figure()
        plt.plot(avg_volume_day)
        plt.title("volum dag")
        plt.figure()
        plt.plot(avg_rvol_day)
        plt.title("volatility dag")
        plt.figure()
        plt.plot(avg_illiq_day)
        plt.title("illiq dag")


if plots == 1:
    plt.show()