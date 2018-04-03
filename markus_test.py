import data_import as di
import data_import_support as dis

bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(exc="bitstampusd")
coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(exc="coinbaseusd")
bitstamp_hour_list, prices, volumes_bitstampH = dis.convert_to_hour(time_list_bitstampM, prices_bitstampM,volumes_bitstampM)
coinbase_hour_list, prices, volumes_coinbaseH = dis.convert_to_hour(time_list_coinbaseM, prices_coinbaseM,volumes_coinbaseM)


#exc_name1,time_list1, returns1, spread1, volumes1, log_volumes1, illiq1, log_illiq1, rvol1, log_rvol1 =di.get_list(exc="bitstampusd", freq="h", local_time=0)
#exc_name2,time_list2, returns2, spread2, volumes2, log_volumes2, illiq2, log_illiq2, rvol2, log_rvol2 =di.get_list(exc="btcncny", freq="h", local_time=0)

print(bitstamp_hour_list[0:10])
print(coinbase_hour_list[0:10])
time_list_combined, volumes_combined = dis.add_two_series_w_different_times(time_list1, volumes1, time_list2, volumes2)


