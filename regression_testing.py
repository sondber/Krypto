import numpy as np
import data_import as di
import data_import_support as dis
import regression_support
from Sondre import sondre_support_formulas as supp

#os.chdir("/Users/Jacob/Documents/GitHub/krypto")

#exc = 1

#exchanges, time_listM, pricesM, volumesM = di.get_lists(opening_hours="n", make_totals="n")
#time_listH, returnsH, spreadH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_trans_hours(time_listM, pricesM, volumesM, exc=exc, convert_time_zones=1)
#complete_time = dis.convert_to_hour(time_listM, pricesM, volumesM)[0]
#print(time_listH[0:48])
#print(complete_time[0:48])

data = [0.1, 0.7, 1.8, 3.4, 4.4, 4.8, 6.0, 7.1, 7.9, 8.7, 10.4, 10.8, 12.5, 12.6, 13.7, 15.1, 16.2, 16.6, 18.0, 18.6, 19.9, 20.5, 22.4, 23.2, 23.8, 25.3, 25.7, 26.8, 28.0, 29.5, 30.1, 30.8, 32.2, 32.9, 34.2, 34.6, 36.4, 36.8, 38.0, 39.1, 39.6, 40.7, 42.2, 43.4, 44.3, 45.1, 45.8, 47.1]

time_test = ['01.06.2016 02:00', '01.06.2016 11:00', '01.06.2016 17:00', '02.06.2016 02:00', '02.06.2016 14:00', '02.06.2016 19:00', '03.06.2016 12:00', '03.06.2016 14:00', '03.06.2016 19:00', '03.06.2016 20:00', '03.06.2016 22:00', '04.06.2016 09:00', '06.06.2016 05:00', '06.06.2016 22:00', '07.06.2016 07:00', '07.06.2016 15:00', '08.06.2016 02:00', '08.06.2016 03:00', '08.06.2016 06:00', '08.06.2016 07:00', '08.06.2016 08:00', '08.06.2016 11:00', '08.06.2016 12:00', '08.06.2016 13:00', '08.06.2016 18:00', '08.06.2016 20:00', '08.06.2016 23:00', '09.06.2016 12:00', '09.06.2016 15:00', '09.06.2016 20:00', '10.06.2016 06:00', '10.06.2016 07:00', '10.06.2016 11:00', '10.06.2016 13:00', '10.06.2016 15:00', '11.06.2016 14:00', '12.06.2016 00:00', '12.06.2016 03:00', '13.06.2016 02:00', '13.06.2016 05:00', '13.06.2016 07:00', '13.06.2016 08:00', '13.06.2016 09:00', '13.06.2016 11:00', '13.06.2016 13:00', '13.06.2016 16:00', '13.06.2016 17:00', '13.06.2016 19:00']
time_easy = ['01.01.2012 00:00', '01.01.2012 01:00', '01.01.2012 02:00', '01.01.2012 03:00', '01.01.2012 04:00', '01.01.2012 05:00', '01.01.2012 06:00', '01.01.2012 07:00', '01.01.2012 08:00', '01.01.2012 09:00', '01.01.2012 10:00', '01.01.2012 11:00', '01.01.2012 12:00', '01.01.2012 13:00', '01.01.2012 14:00', '01.01.2012 15:00', '01.01.2012 16:00', '01.01.2012 17:00', '01.01.2012 18:00', '01.01.2012 19:00', '01.01.2012 20:00', '01.01.2012 21:00', '01.01.2012 22:00', '01.01.2012 23:00', '02.01.2012 00:00', '02.01.2012 01:00', '02.01.2012 02:00', '02.01.2012 03:00', '02.01.2012 04:00', '02.01.2012 05:00', '02.01.2012 06:00', '02.01.2012 07:00', '02.01.2012 08:00', '02.01.2012 09:00', '02.01.2012 10:00', '02.01.2012 11:00', '02.01.2012 12:00', '02.01.2012 13:00', '02.01.2012 14:00', '02.01.2012 15:00', '02.01.2012 16:00', '02.01.2012 17:00', '02.01.2012 18:00', '02.01.2012 19:00', '02.01.2012 20:00', '02.01.2012 21:00', '02.01.2012 22:00', '02.01.2012 23:00']

time_list = time_test

lag_test = 7

lagged_list, index_list = regression_support.get_lagged_list(data, time_list, lag=lag_test)

last_day_average = regression_support.get_last_day_average(data, time_list, index_list, lag=lag_test)

for i in range(len(lagged_list)):
    #print("Index: ", i, "Input:", time_list[i], "Input data:", data[i], "Lagged data:", lagged_list[i], "Index of lag:", index_list[i])
    print("Index: ", i, "Input:", time_list[i], "Input data:", data[i], "Average:", last_day_average[i], "Index of lag:",
          index_list[i])