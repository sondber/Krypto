import numpy as np
import data_import as di
from Sondre import sondre_support_formulas as supp
import data_import_support as dis


def AR_matrix(y, y_time, order, hours_to_remove=[]):
    n = len(y)
    ar_len = n - order

    if order == 1:
        index = np.zeros(n)
        x = np.zeros(ar_len)
        i = n -1

        while i>=0:
            found = 0
            j = i
            while not found and j>=0:
                if supp.fix_time_list(y_time[i], single_time_stamp=1, move_n_hours=-1) == supp.fix_time_list(y_time[j],
                                                                                                             single_time_stamp=1):
                    found = 1
                    index[i] = 1
                    x[i-1] = y[j]
                j -= 1
            if not found:
                index[i] = 0
            i -= 1

    else:
        index = np.zeros([n, order])
        x = np.zeros([ar_len, order])
        for k in range(order):
            i = n - 1
            while i >= k:
                found = 0
                j = i
                while found == 0 and j > 0:
                    if supp.fix_time_list(y_time[i], single_time_stamp=1, move_n_hours=-(k+1)) == supp.fix_time_list(y_time[j],
                                                                                                                 single_time_stamp=1):
                        found = 1
                        index[i, k] = 1
                        x[i-order, k] = y[j]
                    j -= 1
                if found == 0:
                    index[i, k] = 0
                i -= 1

    return index, x


check = 1
lag = 3

exc, time_listM, pricesM, volumesM = di.get_list(-1)
time_listH, pricesH, volumesH = dis.convert_to_hour(time_listM, pricesM, volumesM)

index_test, x_test = AR_matrix(pricesH, time_listH, order=lag)

if check == 1:
    if lag == 1:
        for i in range(0,lag):
            print(time_listH[i], pricesH[i], index_test[i])
        for j in range(0, len(x_test)):
            print(time_listH[j+lag], pricesH[j+lag], index_test[j+lag], x_test[j])
    else:
        col = 0  #HER SJEKKER DU DE ULIKE AR(COL) (husk at 0 er 1)
        for i in range(0, lag):
            print(time_listH[i], pricesH[i], index_test[i,col])
        for j in range(0, len(x_test)):
            print(time_listH[j + lag], pricesH[j + lag], index_test[j + lag, col], x_test[j, col])


