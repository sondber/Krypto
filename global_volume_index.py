import data_import as di
import data_import_support as dis
import csv
import numpy as np
from Sondre import sondre_support_formulas as supp


def write_daily_volume_index_to_csv():
    bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(exc="bitstampusd")
    coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(exc="coinbaseusd")
    korbit, time_list_korbitM, prices_korbitM, volumes_korbitM = di.get_list(exc="korbitkrw")
    krak, time_list_krakM, prices_krakM, volumes_krakM = di.get_list(exc="krakeneur")
    cc, time_list_ccM, prices_ccM, volumes_ccM = di.get_list(exc="coincheckjpy")

    bitstamp_day_list, prices, volumes_bitstampD = dis.convert_to_day(time_list_bitstampM, prices_bitstampM,volumes_bitstampM)
    coinbase_day_list, prices, volumes_coinbaseD = dis.convert_to_day(time_list_coinbaseM, prices_coinbaseM,volumes_coinbaseM)
    korbit_day_list, prices, volumes_korbitD = dis.convert_to_day(time_list_korbitM, prices_korbitM, volumes_korbitM)
    krak_day_list, prices, volumes_krakD = dis.convert_to_day(time_list_krakM, prices_krakM, volumes_krakM)
    cc_day_list, prices, volumes_ccD = dis.convert_to_day(time_list_ccM, prices_ccM, volumes_ccM)


    #
    # time_list_combined, volumes_combined = dis.add_two_series_w_different_times(coinbase_day_list, volumes_coinbaseD, bitstamp_day_list, volumes_bitstampD)
    # time_list_combined, volumes_combined = dis.add_two_series_w_different_times(time_list_combined, volumes_combined, korbit_day_list, volumes_korbitD)
    # time_list_combined, volumes_combined = dis.add_two_series_w_different_times(time_list_combined, volumes_combined, krak_day_list, volumes_krakD)
    # time_list_combined, volumes_combined = dis.add_two_series_w_different_times(cc_day_list, volumes_ccD, time_list_combined, volumes_combined)

    time_list_combined, volumes_combined = dis.fix_gv(bitstamp_day_list, volumes_bitstampD, coinbase_day_list, volumes_coinbaseD, korbit_day_list, volumes_korbitD, krak_day_list, volumes_krakD, cc_day_list, volumes_ccD)


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

def get_global_daily_volume_index(transformed=0):
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


    if transformed == 1:
        start_i = 30
        initial_volume = np.average(volumesD[0:start_i])
        time_listD = time_listD[start_i:]
        volumesD = volumesD[start_i:]
        volumesD = dis.volume_transformation(volumesD, initial_volume, daily=1)

    return time_listD, volumesD


def write_hourly_volume_index_to_csv(print_components=0):
    bitstamp, time_list_bitstampM, prices_bitstampM, volumes_bitstampM = di.get_list(exc="bitstampusd")
    coinbase, time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM = di.get_list(exc="coinbaseusd")
    korbit, time_list_korbitM, prices_korbitM, volumes_korbitM = di.get_list(exc="korbitkrw")
    krak, time_list_krakM, prices_krakM, volumes_krakM = di.get_list(exc="krakeneur")
    cc, time_list_ccM, prices_ccM, volumes_ccM = di.get_list(exc="coincheckjpy")

    bitstamp_hour_list, prices, volumes_bitstampH = dis.convert_to_hour(time_list_bitstampM, prices_bitstampM,volumes_bitstampM)
    coinbase_hour_list, prices, volumes_coinbaseH = dis.convert_to_hour(time_list_coinbaseM, prices_coinbaseM, volumes_coinbaseM)
    korbit_hour_list, prices, volumes_korbitH = dis.convert_to_hour(time_list_korbitM, prices_korbitM, volumes_korbitM)
    krak_hour_list, prices, volumes_krakH = dis.convert_to_hour(time_list_krakM, prices_krakM, volumes_krakM)
    cc_hour_list, prices, volumes_ccH = dis.convert_to_hour(time_list_ccM, prices_ccM, volumes_ccM)



    time_list_combined, volumes_combined = dis.add_two_series_w_different_times(coinbase_hour_list, volumes_coinbaseH, bitstamp_hour_list, volumes_bitstampH)
    time_list_combined, volumes_combined = dis.add_two_series_w_different_times(time_list_combined, volumes_combined, korbit_hour_list, volumes_korbitH)
    time_list_combined, volumes_combined = dis.add_two_series_w_different_times(time_list_combined, volumes_combined, krak_hour_list, volumes_krakH)
    time_list_combined, volumes_combined = dis.add_two_series_w_different_times(cc_hour_list, volumes_ccH, time_list_combined, volumes_combined)

    if print_components == 1:
        total = sum(volumes_bitstampH) + sum(volumes_coinbaseH) + sum(volumes_korbitH) + sum(volumes_krakH) + sum(volumes_ccH)
        # bitstamp_perc = 100 * float(sum(volumes_bitstampH) / total)
        # coinbase_perc = 100 * float(sum(volumes_coinbaseH) / total)
        # korbit_perc = 100 * float(sum(volumes_korbitH) / total)
        # krak_perc = 100 * float(sum(volumes_krakH) / total)
        # cc_perc = 100 * float(sum(volumes_ccH) / total)
        #
        # print("%s approximate share of the total volume")



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


def get_global_hourly_volume_index(transformed=0):
    file_name = 'data/export_csv/global_hourly_volume_index.csv'
    time_listH = []
    volumesH = []

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_listH.append(row[0])
                volumesH.append(float(row[1]))
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            i = i + 1
    print("\033[0;32;0m Finished reading file '%s'...\033[0;0;0m" % file_name)

    if transformed == 1:
        start_i = 720
        initial_volume = np.average(volumesH[0:start_i])
        time_listH = time_listH[start_i:]
        volumesH = volumesH[start_i:]
        volumesH = dis.volume_transformation(volumesH, initial_volume, daily=1)

    return time_listH, volumesH


def remove_holes(time_list_external, time_list_global_volumes, global_volumes):

    print(time_list_external[0:10])
    print(time_list_global_volumes[0:10])
    if supp.A_before_B(time_list_external[0], time_list_global_volumes[0]):
        print("External starts before global")
        ex_first = 1
    else:
        print("Global starts before external")
        ex_first = 0

    i = 0
    j = 0
    j0= 0
    time_list_out = []
    data_out = []
    if ex_first:
        while time_list_global_volumes[i] != time_list_external[j]:
            i += 1
        for j in range(len(time_list_external)):
            while time_list_global_volumes[i] != time_list_external[j]:
                i+=1
            time_list_out.append(time_list_global_volumes[i])
            data_out.append(global_volumes[i])

    else:
        while time_list_global_volumes[i] != time_list_external[j0]:
            j0 += 1

        for j in range(j0, len(time_list_external)):
            while time_list_global_volumes[i] != time_list_external[j]:
                i+=1
            time_list_out.append(time_list_global_volumes[i])
            data_out.append(global_volumes[i])
    return time_list_out, data_out



# for å sjekke om ting blir riktig
# print("combined ",time_list_combined[-778:-768])
# print("combined ",volumes_combined[-778:-768])
# print("coin ",coinbase_hour_list[-3010:-3000])
# print("coin ",volumes_coinbaseH[-3010:-3000])
# print("bits ",bitstamp_hour_list[-3010:-3000])
# print("bits ",volumes_bitstampH[-3010:-3000])
# print("btcn ",btcncny_hour_list[-778:-768])
# print("btcn ",volumes_btcncnyH[-778:-768])
# print("korb ",korbit_hour_list[-3010:-3000])
# print("korb ",volumes_korbitH[-3010:-3000])
# print("krak ",krak_hour_list[-3010:-3000])
# print("krak ",volumes_krakH[-3010:-3000])
# print("cc ",cc_hour_list[-3010:-3000])
# print("cc ",volumes_ccH[-3010:-3000])
#
# exc_name1,time_list1, returns1, spread1, volumes1, log_volumes1, illiq1, log_illiq1, rvol1, log_rvol1 =di.get_list(exc="bitstampusd", freq="h", local_time=0)
# exc_name2,time_list2, returns2, spread2, volumes2, log_volumes2, illiq2, log_illiq2, rvol2, log_rvol2 =di.get_list(exc="btcncny", freq="h", local_time=0)
# time_list1=bitstamp_hour_list[0:10]
# time_list2=coinbase_hour_list[0:10]
   #for å sjekke om ting blir riktig
'''

    print("combined ", time_list_combined[-778:-768])
    print("combined ", volumes_combined[-778:-768])
    print("coin ", coinbase_hour_list[-3010:-3000])
    print("coin ", volumes_coinbaseH[-3010:-3000])
    print("bits ", bitstamp_hour_list[-3010:-3000])
    print("bits ", volumes_bitstampH[-3010:-3000])
    print("btcn ", btcncny_hour_list[-778:-768])
    print("btcn ", volumes_btcncnyH[-778:-768])
    print("korb ", korbit_hour_list[-3010:-3000])
    print("korb ", volumes_korbitH[-3010:-3000])
    print("krak ", krak_hour_list[-3010:-3000])
    print("krak ", volumes_krakH[-3010:-3000])
    print("cc ", cc_hour_list[-3010:-3000])
    print("cc ", volumes_ccH[-3010:-3000])

'''

'''
    print("combined ", time_list_combined[-10:-1])
    print("combined ", volumes_combined[-10:-1])
    print("coin ", coinbase_day_list[-10:-1])
    print("coin ", volumes_coinbaseD[-10:-1])
    print("bits ", bitstamp_day_list[-10:-1])
    print("bits ", volumes_bitstampD[-10:-1])
    print("korb ", volumes_korbitD[-10:-1])
    print("krak ", krak_day_list[-10:-1])
    print("krak ", volumes_krakD[-10:-1])
    print("cc ", cc_day_list[-10:-1])
    print("cc ", volumes_ccD[-10:-1])
'''
