import data_import as di
import data_import_support as dis
import csv



def write_daily_volume_to_csv():
    bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(exc="bitstampusd")
    coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(exc="coinbaseusd")
    # btcncny, time_list_btcncnyM, prices_btcncnyM, volumes_btcncnyM = di.get_list(exc="btcncny")
    korbit, time_list_korbitM, prices_korbitM, volumes_korbitM = di.get_list(exc="korbitkrw")
    krak, time_list_krakM, prices_krakM, volumes_krakM = di.get_list(exc="krakeneur")
    cc, time_list_ccM, prices_ccM, volumes_ccM = di.get_list(exc="coincheckjpy")


    bitstamp_day_list, prices, volumes_bitstampD = dis.convert_to_day(time_list_bitstampM, prices_bitstampM,
                                                                      volumes_bitstampM)
    coinbase_day_list, prices, volumes_coinbaseD = dis.convert_to_day(time_list_coinbaseM, prices_coinbaseM,
                                                                      volumes_coinbaseM)
    # btcncny_day_list, prices, volumes_btcncnyD = dis.convert_to_day(time_list_btcncnyM, prices_btcncnyM,volumes_btcncnyM)
    korbit_day_list, prices, volumes_korbitD = dis.convert_to_day(time_list_korbitM, prices_korbitM, volumes_korbitM)
    krak_day_list, prices, volumes_krakD = dis.convert_to_day(time_list_krakM, prices_krakM, volumes_krakM)
    cc_day_list, prices, volumes_ccD = dis.convert_to_day(time_list_ccM, prices_ccM, volumes_ccM)

    time_list_combined2, volumes_combined2 = dis.add_two_series_w_different_times(coinbase_day_list, volumes_coinbaseD,
                                                                                  bitstamp_day_list, volumes_bitstampD)
    # time_list_combined1, volumes_combined1 = dis.add_two_series_w_different_times(time_list_combined2, volumes_combined2,btcncny_day_list, volumes_btcncnyD)
    time_list_combined0, volumes_combined0 = dis.add_two_series_w_different_times(time_list_combined2,
                                                                                  volumes_combined2, korbit_day_list,
                                                                                  volumes_korbitD)
    time_list_combined00, volumes_combined00 = dis.add_two_series_w_different_times(time_list_combined0,
                                                                                    volumes_combined0, krak_day_list,
                                                                                    volumes_krakD)
    time_list_combined, volumes_combined = dis.add_two_series_w_different_times(cc_day_list, volumes_ccD,
                                                                                time_list_combined00,
                                                                                volumes_combined00)
    location = "data/export_csv/"
    file_name = location + "global_daily_volume_index.csv"
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

def get_global_daily_volume():
    file_name = 'data/export_csv/global_daily_volume_index.csv'
    time_listD = []
    volumesD = []

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_listD.append(row[0])
                volumesD.append(float(row[1]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
    print("\033[0;32;0m Finished reading file '%s'...\033[0;0;0m" % file_name)
    return time_listD, volumesD


def write_hourly_volume_to_csv():
    bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(exc="bitstampusd")
    coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(exc="coinbaseusd")
    btcncny, time_list_btcncnyM, prices_btcncnyM, volumes_btcncnyM = di.get_list(exc="btcncny")
    korbit, time_list_korbitM, prices_korbitM, volumes_korbitM = di.get_list(exc="korbitkrw")
    krak, time_list_krakM, prices_krakM, volumes_krakM = di.get_list(exc="krakeneur")
    cc, time_list_ccM, prices_ccM, volumes_ccM = di.get_list(exc="coincheckjpy")

    bitstamp_hour_list, prices, volumes_bitstampH = dis.convert_to_hour(time_list_bitstampM, prices_bitstampM,volumes_bitstampM)
    coinbase_hour_list, prices, volumes_coinbaseH = dis.convert_to_hour(time_list_coinbaseM, prices_coinbaseM,volumes_coinbaseM)
    btcncny_hour_list, prices, volumes_btcncnyH = dis.convert_to_hour(time_list_btcncnyM, prices_btcncnyM,volumes_btcncnyM)
    korbit_hour_list, prices, volumes_korbitH = dis.convert_to_hour(time_list_korbitM, prices_korbitM,volumes_korbitM)
    krak_hour_list, prices, volumes_krakH = dis.convert_to_hour(time_list_krakM, prices_krakM,volumes_krakM)
    cc_hour_list, prices, volumes_ccH = dis.convert_to_hour(time_list_ccM, prices_ccM,volumes_ccM)

    time_list_combined2, volumes_combined2 = dis.add_two_series_w_different_times(coinbase_hour_list, volumes_coinbaseH,bitstamp_hour_list, volumes_bitstampH)
    time_list_combined1, volumes_combined1 = dis.add_two_series_w_different_times(time_list_combined2, volumes_combined2,btcncny_hour_list, volumes_btcncnyH)
    time_list_combined0, volumes_combined0 = dis.add_two_series_w_different_times(time_list_combined1, volumes_combined1,korbit_hour_list, volumes_korbitH)
    time_list_combined00, volumes_combined00 = dis.add_two_series_w_different_times(time_list_combined0, volumes_combined0,krak_hour_list, volumes_krakH)
    time_list_combined, volumes_combined = dis.add_two_series_w_different_times(cc_hour_list, volumes_ccH,time_list_combined00, volumes_combined00)

    location = "data/export_csv/"
    file_name = location + "global_hourly_volume_index.csv"
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


def get_global_hourly_volume():
    file_name = 'data/export_csv/global_hourly_volume_index.csv'
    time_listD = []
    volumesD = []

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_listD.append(row[0])
                volumesD.append(float(row[1]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
    print("\033[0;32;0m Finished reading file '%s'...\033[0;0;0m" % file_name)
    return time_listD, volumesD

'''   #for å sjekke om ting blir riktig     
print("combined ",time_list_combined[-778:-768])
print("combined ",volumes_combined[-778:-768])
print("coin ",coinbase_hour_list[-3010:-3000])
print("coin ",volumes_coinbaseH[-3010:-3000])
print("bits ",bitstamp_hour_list[-3010:-3000])
print("bits ",volumes_bitstampH[-3010:-3000])
print("btcn ",btcncny_hour_list[-778:-768])
print("btcn ",volumes_btcncnyH[-778:-768])
print("korb ",korbit_hour_list[-3010:-3000])
print("korb ",volumes_korbitH[-3010:-3000])
print("krak ",krak_hour_list[-3010:-3000])
print("krak ",volumes_krakH[-3010:-3000])
print("cc ",cc_hour_list[-3010:-3000])
print("cc ",volumes_ccH[-3010:-3000])
'''


#exc_name1,time_list1, returns1, spread1, volumes1, log_volumes1, illiq1, log_illiq1, rvol1, log_rvol1 =di.get_list(exc="bitstampusd", freq="h", local_time=0)
#exc_name2,time_list2, returns2, spread2, volumes2, log_volumes2, illiq2, log_illiq2, rvol2, log_rvol2 =di.get_list(exc="btcncny", freq="h", local_time=0)
#time_list1=bitstamp_hour_list[0:10]
#time_list2=coinbase_hour_list[0:10]