import data_import as di
import plot
from Jacob import jacob_support as jake_supp
import data_import_support as dis

spec = "01012015_6"
intraday = 0
intraweek = 1

exch = [0]  # 0=bitstamp, 1=coincheck

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")

for exc in exch:
    exc_name = "_" + exchanges[exc] + "_TEST_" + spec
    print()
    print("SEASONALITY FOR", exchanges[exc].upper())

    if intraday == 1:
        # HOURS ----------------------------------------------------------------------------------------------------
        print("------ INTRADAY  ------")

        time_list_hours, returns_hours, spread_hours, log_volumes_hours, illiq_hours, \
        illiq_hours_time, log_illiq_hours, rvol_hours, log_rvol_hours = \
            dis.clean_series_hour(time_list_minutes, prices_minutes, volumes_minutes, exc=exc, convert_time_zones=1)

        # Finding average for every hour of the day
        hour_of_day, avg_volumes_hour, low_volumes_hour, upper_volumes_hour = dis.cyclical_average(time_list_hours, log_volumes_hours, frequency="h")
        hour_of_day, avg_spread_hour, low_spread_hour, upper_spread_hour = dis.cyclical_average(time_list_hours, spread_hours, frequency="h")
        hour_of_day, avg_illiq_hour, low_illiq_hour, upper_illiq_hour = dis.cyclical_average(time_list_hours, illiq_hours, frequency="h")
        #hour_of_day, avg_log_illiq_hour, low_log_illiq_hour, upper_log_illiq_hour = dis.cyclical_average(illiq_timeH, log_illiq_hours, frequency="h")

        plot.intraday(avg_volumes_hour, low_volumes_hour, upper_volumes_hour, title="Log_Volume" + exc_name, perc=0)
        plot.intraday(avg_spread_hour, low_spread_hour, upper_spread_hour, title="Spread" + exc_name, perc=1)
        plot.intraday(avg_illiq_hour, low_illiq_hour, upper_illiq_hour, title="ILLIQ" + exc_name, perc=1, ndigits=2)
        #plot.intraday(avg_log_illiq_hour, low_log_illiq_hour, upper_log_illiq_hour, title="Log_ILLIQ" + exc_name, perc=0, ndigits=3, logy=0)  # Skulle helst brukt vanlig illiq med log-skala i stedet

    if intraweek == 1:
        print("------ INTRAWEEK ------")
        # DAYS ----------------------------------------------------------------------------------------------------
        # Converting to daily data
        returns_minutes = jake_supp.logreturn(prices_minutes[exc, :])
        time_list_days, time_list_removed, returns_days, volumes_days, log_volumes_days, spread_days, \
        illiq_days, log_illiq_days, rvol_days, log_rvol_days = dis.clean_series_days(
            time_list_minutes, prices_minutes, volumes_minutes, exc=exc, print_days_excluded=0, convert_time_zones=1)

        day_of_week, avg_spread_day, low_spread_day, upper_spread_day = dis.cyclical_average(time_list_days, spread_days, frequency="d")
        day_of_week, avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean = dis.cyclical_average(time_list_days, illiq_days, frequency="d")
        plot.intraweek(avg_spread_day, low_spread_day, upper_spread_day, title="Spread" + exc_name, perc=1, ndigits=3)
        plot.intraweek(avg_illiq_day_clean, low_illiq_day_clean, upper_illiq_day_clean, title="ILLIQ" + exc_name, perc=1,   logy=0, ndigits=3)

        # Finding average for transformed
        day_of_week, avg_log_volume_day, low_log_volume_day, upper_log_volume_day = dis.cyclical_average(time_list_days, log_volumes_days, frequency="d")
        #day_of_week, avg_log_illiq_day, low_log_illiq_day, upper_log_illiq_day = dis.cyclical_average(time_list_days, log_illiq_days, frequency="d")

        #plot.intraweek(avg_log_illiq_day, low_log_illiq_day, upper_log_illiq_day, title="Log_ILLIQ" + exc_name, perc=0,   logy=0, ndigits=3)
        plot.intraweek(avg_log_volume_day, low_log_volume_day, upper_log_volume_day, title="Log_Volume" + exc_name, perc=0,weekends=1)  # Hva faen gjør vi med y-aksen på denne?
