import data_import as di
import data_import_support as dis
import csv

bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(exc="bitstampusd")
coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(exc="coinbaseusd")
bitstamp_hour_list, prices, volumes_bitstampH = dis.convert_to_hour(time_list_bitstampM, prices_bitstampM,volumes_bitstampM)
coinbase_hour_list, prices, volumes_coinbaseH = dis.convert_to_hour(time_list_coinbaseM, prices_coinbaseM,volumes_coinbaseM)


#exc_name1,time_list1, returns1, spread1, volumes1, log_volumes1, illiq1, log_illiq1, rvol1, log_rvol1 =di.get_list(exc="bitstampusd", freq="h", local_time=0)
#exc_name2,time_list2, returns2, spread2, volumes2, log_volumes2, illiq2, log_illiq2, rvol2, log_rvol2 =di.get_list(exc="btcncny", freq="h", local_time=0)
#time_list1=bitstamp_hour_list[0:10]
#time_list2=coinbase_hour_list[0:10]


time_list_combined, volumes_combined = dis.add_two_series_w_different_times(coinbase_hour_list, volumes_coinbaseH,bitstamp_hour_list, volumes_bitstampH)
#time_list_combined, volumes_combined = dis.add_two_series_w_different_times(bitstamp_hour_list, volumes_bitstampH,coinbase_hour_list, volumes_coinbaseH)
print("combined ",time_list_combined[-1010:-1000])
print("combined ",volumes_combined[-1010:-1000])
print("coin ",coinbase_hour_list[-1010:-1000])
print("coin ",volumes_coinbaseH[-1010:-1000])
print("bits ",bitstamp_hour_list[-1010:-1000])
print("bits ",volumes_bitstampH[-1010:-1000])


location = "data/export_csv/"
file_name = location + "global_volume_index.csv"
with open(file_name, 'w', newline='') as csvfile:
    writ = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    print("\033[0;32;0m Writing to file '%s'...\033[0;0;0m" % file_name)
    header2 = ["Time"]
    header2.append("Volume")

    writ.writerow(header2)

    for i in range(len(volumes_combined)):
        rowdata = [time_list_combined[i]]
        rowdata.append(volumes_combined[i])
        writ.writerow(rowdata)