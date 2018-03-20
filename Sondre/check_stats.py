import numpy as np
import data_import as di
import legacy
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


def add_to_row(print_rows, output, i):
    print_rows.append(output[0])
    for j in range(1, len(output)):
        print_rows[i] += "   &   "
        data = output[j]
        if data >= 1000:
            data_string = str(int(data))
        elif data >= 10:
            data_string = str("{0:.2f}".format(data))
        else:
            data_string = str("{0:.3f}".format(data))
        print_rows[i] += data_string
    i += 1
    return print_rows, i


os.chdir("/Users/sondre/Documents/GitHub/krypto")

exc=0  # Bitstamp

#RAW
raw = 1
combined = 1

exchanges, time_list_minutes, prices_minutes, volumes_minutes = legacy.get_lists_legacy(opening_hours="n", make_totals="n")

print()
raw = 0
clean = 1

if raw == 1:
    # RAW
    time_list_days, prices_days, volumes_days = dis.convert_to_day(time_list_minutes, prices_minutes, volumes_minutes)
    returns_minutes = jake_supp.logreturn(prices_minutes[exc, :])
    returns_days = jake_supp.logreturn(prices_days[exc, :])
    spread_days = rolls.rolls(prices_minutes[exc, :], time_list_minutes, calc_basis=1, kill_output=1)[1]
    illiq_days_time, illiq_days = ILLIQ.illiq(time_list_minutes, returns_minutes, volumes_minutes[exc, :], hourly_or_daily=1)

    # Realized volatility
    volatility_days, rVol_time = realized_volatility.RVol(time_list_minutes, prices_minutes[exc, :])
    # Annualize the volatility
    volatility_days = np.multiply(volatility_days, 365 ** 0.5)


    print("RAW------------------------------------------")
    print("Number of entries in RAW:", len(returns_days))
    desc.stats_for_single_list(volumes_days[exc, :], "Volumes RAW")
    desc.stats_for_single_list(returns_days, "Returns RAW")
    desc.stats_for_single_list(volatility_days, "RVol, annualized RAW")
    desc.stats_for_single_list(spread_days, "Roll's RAW")
    desc.stats_for_single_list(illiq_days, "ILLIQ RAW")
    print("RAW END--------------------------------------")


if clean == 1:
    # CLEAN
    time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
    illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_series_days(
        time_list_minutes, prices_minutes,
        volumes_minutes, full_week=1, exc=exc)

    print_rows = []
    i = 0
    print_rows.append("Variables     &    Min    &   Max      &   $\\mu$    &   $\\sigma$    &  Kurtosis  &  Skewness  &   $AC_1$   &    $AC_{10}$   &   n ")
    i += 1

    output = desc.stats_for_single_list(volumes_days_clean, "$V$        ")
    print_rows, i = add_to_row(print_rows, output, i)

    output = desc.stats_for_single_list(returns_days_clean, "$r$        ")
    print_rows, i = add_to_row(print_rows, output, i)

    output = desc.stats_for_single_list(volatility_days_clean, "RVol, annualized") #<---------------HER !!!!!
    print_rows.append("$RV$       ")
    print_rows, i = add_to_row(print_rows, output, i)

    output = desc.stats_for_single_list(spread_days_clean, "Roll's")
    print_rows.append("$bas$      ")
    print_rows, i = add_to_row(print_rows, output, i)

    desc.stats_for_single_list(illiq_days_clean, "ILLIQ")
    print_rows.append("$illiq$    ")
    print_rows, i = add_to_row(print_rows, output, i)

    desc.stats_for_single_list(log_volumes_days_clean, "Log Volumes")
    desc.stats_for_single_list(log_illiq_days_clean, "Log ILLIQ")
    desc.stats_for_single_list(log_volatility_days_clean, "RVol, annualized")

    print("     ------SUMMARY STATISTICS FOR"+exchanges[exc].upper()+"--------------")
    for k in range(0, len(print_rows)):
        print(print_rows[k])
