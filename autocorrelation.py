import numpy as np
from Sondre import sondre_support_formulas as supp
import data_import as di
import data_import_support as dis


def write_autocorr(variable, name="varible"):
    intro = "Autocorrelation analysis for: "
    print(intro + name)
    for lag in range(1, 13):
        corr = supp.autocorr(variable, lag)
        print(" %i days lag: %0.2f%%" % (lag, corr * 100))
    print()
    print()


exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="y", make_totals="n")
time_list_days_clean, time_list_removed, returns_days_clean, volumes_days_clean, log_volumes_days_clean, spread_days_clean, \
illiq_days_clean, log_illiq_days_clean, volatility_days_clean, log_volatility_days_clean = dis.clean_trans_days(
    time_list_minutes, prices_minutes,
    volumes_minutes)

print()
write_autocorr(spread_days_clean, "BAS")
write_autocorr(illiq_days_clean, "ILLIQ")
write_autocorr(log_illiq_days_clean, "Log ILLIQ")
write_autocorr(volatility_days_clean, "Volatility")
write_autocorr(log_volatility_days_clean, "Log volatility")

