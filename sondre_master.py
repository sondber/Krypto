import data_import as di
import plot
import user_interface as ui
import sondre_support_formulas as supp
# import numpy as np


# ------------------------------------------------------------
# To fetch lists:
# ----------------
# exchanges, time_list, prices, volumes, total_price, total_volume, currency = di.get_lists(which_freq, which_loc, startdate, enddate)
# which_freq    -       0=daily, 1=hourly, 2=minute
# which_loc     -       0=raw csvs, 1=aggregate csv
# ------------------------------------------------------------

startdate = "201301"
enddate = "201709"

# ----------------------------------------------------------------------------------------
automatic_fetch = 1  # <--------- set to '0' if you want manual control, '1' for automatic
if automatic_fetch == 1:    # hvis du vil slippe user interface
    which_freq = 2
    which_loc = 1
    print("Gahtering minute data for Bitstamp from aggregate csv..")
else:
    which_freq, which_loc = ui.where_to_get_data()

exchanges, time_list, prices, volumes, total_price, total_volume, currency = di.get_lists(which_freq, which_loc, startdate, enddate)
# ----------------------------------------------------------------------------------------


# --------------------------------------------------------------------------
ask_for_plots = 0  # <--------- set to '1' if you want to generate plots
if ask_for_plots == 1:
    plot.user_plots(exchanges, time_list, prices, volumes, total_price, total_volume, currency)
else:
    print("Did not ask for plots")
# --------------------------------------------------------------------------


x = total_volume
y = total_price
plot.scatters(x, y)


"""
analysis = 0
if analysis:
    print("DATA ANALYSIS")
    print("---------------------------------------------------------------------------------\n")
    number_of_intervals = 10
    for i in range(0, n_exc):
        print("Exchange: " + exchanges[i])
        print("--------------------------")
        supp.data_analysis(volumes[i, :], number_of_intervals)
        print("--------------------------")
    print()
    print()
"""  # not finished