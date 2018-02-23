import os
import numpy as np

import Sondre.sondre_support_formulas
import data_import as di
import data_import_support as dis
import linreg
from Sondre import sondre_support_formulas as supp
import plot
from Jacob import jacob_support as jake_supp
import data_import_support as dis
import rolls
import ILLIQ
import realized_volatility


# Only one of these can be 1
twenty_four_hours = 0
three_periods = 1
four_periods = 0

exc = 1
exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")
# Converting to hourly data
time_list_hours, prices_hours, volumes_hours = dis.convert_to_hour(time_list_minutes, prices_minutes, volumes_minutes)

time_list_hours_clean, returns_hours_clean, spread_hours_clean, log_volumes_hours_clean, illiq_hours_clean, \
    illiq_hours_time, log_illiq_hours_clean = \
    dis.clean_trans_hours(time_list_minutes, prices_minutes, volumes_minutes, exc=exc)

hour = supp.fix_time_list(time_list_hours_clean)[3]
hour_illiq = supp.fix_time_list(illiq_hours_time)[3]

mean_volume = np.mean(log_volumes_hours_clean)
mean_spread = np.mean(spread_hours_clean)
mean_illiq = np.mean(log_illiq_hours_clean)
mean_return = np.mean(returns_hours_clean)

log_volumes_hours_clean -= mean_volume
spread_hours_clean -= mean_spread
log_illiq_hours_clean -= mean_illiq
returns_hours_clean -= mean_return


n = len(hour)
n_illiq = len(hour_illiq)

if twenty_four_hours == 1:
    zero = np.zeros(n)
    one = np.zeros(n)
    two = np.zeros(n)
    three = np.zeros(n)
    four = np.zeros(n)
    five = np.zeros(n)
    six = np.zeros(n)
    seven = np.zeros(n)
    eight = np.zeros(n)
    nine = np.zeros(n)
    ten = np.zeros(n)
    eleven = np.zeros(n)
    twelve = np.zeros(n)
    thirteen = np.zeros(n)
    fourteen = np.zeros(n)
    fifteen = np.zeros(n)
    sixteen = np.zeros(n)
    seventeen = np.zeros(n)
    eighteen = np.zeros(n)
    nineteen = np.zeros(n)
    twenty = np.zeros(n)
    twentyone = np.zeros(n)
    twentytwo = np.zeros(n)
    twentythree = np.zeros(n)


    zero_illiq = np.zeros(n_illiq)
    one_illiq = np.zeros(n_illiq)
    two_illiq = np.zeros(n_illiq)
    three_illiq = np.zeros(n_illiq)
    four_illiq = np.zeros(n_illiq)
    five_illiq = np.zeros(n_illiq)
    six_illiq = np.zeros(n_illiq)
    seven_illiq = np.zeros(n_illiq)
    eight_illiq = np.zeros(n_illiq)
    nine_illiq = np.zeros(n_illiq)
    ten_illiq = np.zeros(n_illiq)
    eleven_illiq = np.zeros(n_illiq)
    twelve_illiq = np.zeros(n_illiq)
    thirteen_illiq = np.zeros(n_illiq)
    fourteen_illiq = np.zeros(n_illiq)
    fifteen_illiq = np.zeros(n_illiq)
    sixteen_illiq = np.zeros(n_illiq)
    seventeen_illiq = np.zeros(n_illiq)
    eighteen_illiq = np.zeros(n_illiq)
    nineteen_illiq = np.zeros(n_illiq)
    twenty_illiq = np.zeros(n_illiq)
    twentyone_illiq = np.zeros(n_illiq)
    twentytwo_illiq = np.zeros(n_illiq)
    twentythree_illiq = np.zeros(n_illiq)

    for i in range(0, n):
        hr = hour[i]
        if hr == 0:
            zero[i] = 1
        elif hr == 1:
            one[i] = 1
        elif hr == 2:
            two[i] = 1
        elif hr == 3:
            three[i] = 1
        elif hr == 4:
            four[i] = 1
        elif hr == 5:
            five[i] = 1
        elif hr == 6:
            six[i] = 1
        elif hr == 7:
            seven[i] = 1
        elif hr == 8:
            eight[i] = 1
        elif hr == 9:
            nine[i] = 1
        elif hr == 10:
            ten[i] = 1
        elif hr == 11:
            eleven[i] = 1
        elif hr == 12:
            twelve[i] = 1
        elif hr == 13:
            thirteen[i] = 1
        elif hr == 14:
            fourteen[i] = 1
        elif hr == 15:
            fifteen[i] = 1
        elif hr == 16:
            sixteen[i] = 1
        elif hr == 17:
            seventeen[i] = 1
        elif hr == 18:
            eighteen[i] = 1
        elif hr == 19:
            nineteen[i] = 1
        elif hr == 20:
            twenty[i] = 1
        elif hr == 21:
            twentyone[i] = 1
        elif hr == 22:
            twentytwo[i] = 1
        elif hr == 23:
            twentythree[i] = 1


    for i in range(0, n_illiq):
        hr = hour_illiq[i]
        if hr == 0:
            zero_illiq[i] = 1
        elif hr == 1:
            one_illiq[i] = 1
        elif hr == 2:
            two_illiq[i] = 1
        elif hr == 3:
            three_illiq[i] = 1
        elif hr == 4:
            four_illiq[i] = 1
        elif hr == 5:
            five_illiq[i] = 1
        elif hr == 6:
            six_illiq[i] = 1
        elif hr == 7:
            seven[i] = 1
        elif hr == 8:
            eight_illiq[i] = 1
        elif hr == 9:
            nine_illiq[i] = 1
        elif hr == 10:
            ten_illiq[i] = 1
        elif hr == 11:
            eleven_illiq[i] = 1
        elif hr == 12:
            twelve_illiq[i] = 1
        elif hr == 13:
            thirteen_illiq[i] = 1
        elif hr == 14:
            fourteen_illiq[i] = 1
        elif hr == 15:
            fifteen_illiq[i] = 1
        elif hr == 16:
            sixteen_illiq[i] = 1
        elif hr == 17:
            seventeen_illiq[i] = 1
        elif hr == 18:
            eighteen_illiq[i] = 1
        elif hr == 19:
            nineteen_illiq[i] = 1
        elif hr == 20:
            twenty_illiq[i] = 1
        elif hr == 21:
            twentyone_illiq[i] = 1
        elif hr == 22:
            twentytwo_illiq[i] = 1
        elif hr == 23:
            twentythree_illiq[i] = 1


    X = np.matrix(one)
    X = np.append(X, np.matrix(two), axis=0)
    X = np.append(X, np.matrix(three), axis=0)
    X = np.append(X, np.matrix(four), axis=0)
    X = np.append(X, np.matrix(five), axis=0)
    X = np.append(X, np.matrix(six), axis=0)
    X = np.append(X, np.matrix(seven), axis=0)
    X = np.append(X, np.matrix(eight), axis=0)
    X = np.append(X, np.matrix(nine), axis=0)
    X = np.append(X, np.matrix(ten), axis=0)
    X = np.append(X, np.matrix(eleven), axis=0)
    X = np.append(X, np.matrix(twelve), axis=0)
    X = np.append(X, np.matrix(thirteen), axis=0)
    X = np.append(X, np.matrix(fourteen), axis=0)
    X = np.append(X, np.matrix(fifteen), axis=0)
    X = np.append(X, np.matrix(sixteen), axis=0)
    X = np.append(X, np.matrix(seventeen), axis=0)
    X = np.append(X, np.matrix(eighteen), axis=0)
    X = np.append(X, np.matrix(nineteen), axis=0)
    X = np.append(X, np.matrix(twenty), axis=0)
    X = np.append(X, np.matrix(twentyone), axis=0)
    X = np.append(X, np.matrix(twentytwo), axis=0)
    X = np.append(X, np.matrix(twentythree), axis=0)
    X = np.transpose(X)


    X_illiq = np.matrix(one_illiq)
    X_illiq = np.append(X_illiq, np.matrix(two_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(three_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(four_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(five_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(six_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(seven_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(eight_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(nine_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(ten_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(eleven_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(twelve_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(thirteen_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(fourteen_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(fifteen_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(sixteen_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(seventeen_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(eighteen_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(nineteen_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(twenty_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(twentyone_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(twentytwo_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(twentythree_illiq), axis=0)
    X_illiq = np.transpose(X_illiq)

    n_rows = 51  # in final table
    n_entries = 24  # Må bare være minst like stor som antall forklaringsvariable

elif three_periods == 1:
    first = np.zeros(n)
    second = np.zeros(n)
    third = np.zeros(n)
    first_illiq = np.zeros(n_illiq)
    second_illiq = np.zeros(n_illiq)
    third_illiq = np.zeros(n_illiq)

    first_period = [2, 3, 4, 5, 6, 7, 8, 9]
    second_period = [10, 11, 12, 13, 14, 15, 16, 17]
    third_period = [18, 19, 20, 21, 22, 23, 0, 1]

    for i in range(0, n):
        hr = hour[i]
        if hr in first_period:
            first[i] = 1
        elif hr in second_period:
            second[i] = 1
        elif hr in third_period:
            third[i] = 1

    for i in range(0, n_illiq):
        hr = hour_illiq[i]
        if hr in first_period:
            first_illiq[i] = 1
        elif hr in second_period:
            second_illiq[i] = 1
        elif hr in third_period:
            third_illiq[i] = 1

    X = np.matrix(first)
    X = np.append(X, np.matrix(second), axis=0)
    X = np.append(X, np.matrix(third), axis=0)
    X = np.transpose(X)

    X_illiq = np.matrix(first_illiq)
    X_illiq = np.append(X_illiq, np.matrix(second_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(third_illiq), axis=0)
    X_illiq = np.transpose(X_illiq)

    n_rows = 9  # in final table
    n_entries = 3  # Må bare være minst like stor som antall forklaringsvariable

elif four_periods == 1:
    first = np.zeros(n)
    second = np.zeros(n)
    third = np.zeros(n)
    fourth = np.zeros(n)
    first_illiq = np.zeros(n_illiq)
    second_illiq = np.zeros(n_illiq)
    third_illiq = np.zeros(n_illiq)
    fourth_illiq = np.zeros(n_illiq)

    first_period = [0, 1, 2, 3, 4, 5]
    second_period = [6, 7, 8, 9, 10, 11]
    third_period = [12, 13, 14, 15, 16, 17]
    fourth_period = [18, 19, 20, 21, 22, 23]

    for i in range(0, n):
        hr = hour[i]
        if hr in first_period:
            first[i] = 1
        elif hr in second_period:
            second[i] = 1
        elif hr in third_period:
            third[i] = 1
        elif hr in fourth_period:
            fourth[i] = 1

    for i in range(0, n_illiq):
        hr = hour_illiq[i]
        if hr in first_period:
            first_illiq[i] = 1
        elif hr in second_period:
            second_illiq[i] = 1
        elif hr in third_period:
            third_illiq[i] = 1
        elif hr in fourth_period:
            fourth_illiq[i] = 1


    X = np.matrix(first)
    X = np.append(X, np.matrix(second), axis=0)
    X = np.append(X, np.matrix(third), axis=0)
    X = np.append(X, np.matrix(fourth), axis=0)
    X = np.transpose(X)

    X_illiq = np.matrix(first_illiq)
    X_illiq = np.append(X_illiq, np.matrix(second_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(third_illiq), axis=0)
    X_illiq = np.append(X_illiq, np.matrix(fourth_illiq), axis=0)
    X_illiq = np.transpose(X_illiq)


    n_rows = 11  # in final table
    n_entries = 4  # Må bare være minst like stor som antall forklaringsvariable


n_cols = 4
coeff_matrix = np.zeros([n_entries, n_cols])
rsquared_array = np.zeros(n_cols)
aic_array = np.zeros(n_cols)
n_obs_array = np.zeros(n_cols)
p_values_matrix = np.zeros([n_entries, n_cols])
std_errs_matrix = np.zeros([n_entries, n_cols])

m_col = 0

Y = returns_hours_clean
m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(
    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=0)
Y = log_volumes_hours_clean
m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(
    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=0)
Y = spread_hours_clean
m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(
    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=0)
Y = illiq_hours_clean
m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(
    m_col, Y, X_illiq, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=0)


if twenty_four_hours == 1:
    first_col_entries = ['00', '01', '02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']
elif three_periods == 1:
    first_col_entries = ['02:00-09:59','10:00-17:59', '18:00-01:59', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']
elif four_periods == 1:
    first_col_entries = ['00:00-05:59','06:00-11:59', '12:00-17:59', '18:00-23:59', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']


first_col = []
j = 0
for i in range(0, len(first_col_entries)):
    first_col.append(first_col_entries[i])
    for k in range(len(first_col_entries[i]), 18):  # Tallet her skal være lengden på den lengste entrien (string)
        first_col[j] += ' '  # Passer på at alle blir like lange
    j += 1
    if i < (n_rows-3)/2:
        first_col.append('                  ')  # De første 24 radene skal ha mellomrom mellom seg
        j += 1

print()

print_rows = []
# Fyller starten med tomromm så det blir lettere å se
for i in range(0, n_rows):
    print_rows.append('        ')
for r in range(0, n_rows):
    print_rows[r] += (first_col[r]) + "&"

i = 0
for r in range(0, n_rows-3, 2):
    for c in range(0, n_cols):
        print_rows[r] = supp.fmt_print(print_rows[r], coeff_matrix[i, c], p_values_matrix[i, c], type="coeff")
        print_rows[r + 1] = supp.fmt_print(print_rows[r + 1], std_errs_matrix[i, c], type="std_err")
    i += 1


# Dette fikser de tre nedreste radene
print_rows[n_rows - 3] += "   "
print_rows[n_rows - 2] += "   "
print_rows[n_rows - 1] += "   "

for c in range(0, n_cols):
    print_rows[n_rows - 3] += str(int(n_obs_array[c])) + "   & "
    print_rows[n_rows - 2] += "{0:.3f}".format(max(rsquared_array[c], 0)) + "   & "
    print_rows[n_rows - 1] += str(int(aic_array[c])) + "  & "
    print_rows[n_rows - 3] += "  "
    print_rows[n_rows - 2] += "  "
    print_rows[n_rows - 1] += "  "

print()
print("     ------------------------------------------------", str(exchanges[exc]),
      "-----------------------------------------")
print()
print(
    "     ------------------------------------------------Regression table for Intraday seasonality-----------------------------------------")
print()
print()
for i in range(0, len(print_rows)):
    if i < len(print_rows) - 3:
        print(
            print_rows[i][0:len(print_rows[i]) - 3] + "\\\\")  # Fjerner det siste &-tegnet og legger til backslash
    else:
        print(
            print_rows[i][0:len(print_rows[i]) - 6] + "\\\\")  # Fjerner det siste &-tegnet og legger til backslash

