import data_import as di
import data_import_support as dis

bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(exc="bitstampusd")
coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(exc="coinbaseusd")
bitstamp_hour_list, prices, volumes_bitstampH = dis.convert_to_hour(time_list_bitstampM, prices_bitstampM,volumes_bitstampM)
coinbase_hour_list, prices, volumes_coinbaseH = dis.convert_to_hour(time_list_coinbaseM, prices_coinbaseM,volumes_coinbaseM)


#exc_name1,time_list1, returns1, spread1, volumes1, log_volumes1, illiq1, log_illiq1, rvol1, log_rvol1 =di.get_list(exc="bitstampusd", freq="h", local_time=0)
#exc_name2,time_list2, returns2, spread2, volumes2, log_volumes2, illiq2, log_illiq2, rvol2, log_rvol2 =di.get_list(exc="btcncny", freq="h", local_time=0)
#time_list1=bitstamp_hour_list[0:10]
#time_list2=coinbase_hour_list[0:10]


time_list_combined, volumes_combined = dis.add_two_series_w_different_times(bitstamp_hour_list, volumes_bitstampH, coinbase_hour_list, volumes_coinbaseH)
print("combined ",time_list_combined[-10:-1])
print("combined ",volumes_combined[-10:-1])
print("coin ",coinbase_hour_list[-10:-1])
print("coin ",volumes_coinbaseH[-10:-1])
print("bits ",bitstamp_hour_list[-10:-1])
print("bits ",volumes_bitstampH[-10:-1])

