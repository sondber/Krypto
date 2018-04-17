import numpy as np
from inspect import currentframe, getframeinfo
from matplotlib import pyplot as plt
import data_import
import data_import as di
import data_import_support as dis
import legacy
import regression_support as rs
from Sondre import sondre_support_formulas as supp
from Jacob import jacob_support as jake_supp
from inspect import getframeinfo as gf, currentframe as cf
import global_volume_index as gvi

# 1 kontrollpanel
log_illiqs = 0 # Should log-illiq be used rather than plain illiq?
hours_in_period = 3 # 2, 3 or 4 hours in dummies
standardized_coeffs = 1 # Should be 1

print_all = 0
intercept = 0
include_global_volumes = True

local_time = 0
spread_determinants = 1  # perform analysis on determinants of spread
illiq_determinants = 0

exchanges = ["bitstamp", "coinbase", "btcn", "korbit"]
exchanges = ["bitstamp", "coinbase"]

n_cols = len(exchanges)*2
n_entries = n_cols * 3  # greit så lenge den er stor nok, si
coeff_matrix = np.zeros([n_entries, n_cols])
rsquared_array = np.zeros(n_cols)
aic_array = np.zeros(n_cols)
n_obs_array = np.zeros(n_cols)
p_values_matrix = np.zeros([n_entries, n_cols])
std_errs_matrix = np.zeros([n_entries, n_cols])


for exc in exchanges:
    exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = di.get_list(exc=exc, freq='h', local_time=local_time)
    time_list_global_volumesH, global_volumesH = gvi.get_global_hourly_volume_index(transformed=1)

    if include_global_volumes:
        time_list_global_volumesH, global_volumesH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.fix_different_time_lists(time_list_global_volumesH, global_volumesH, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH)
        time_listH = time_list_global_volumesH

    for i in range(len(returnsH)):
        returnsH[i] = abs(returnsH[i])

    if log_illiqs == 1:
        illiqH = log_illiqH

    print(" Standardizing all series")
    print()
    log_volumesH = supp.standardize(log_volumesH)
    spreadH = supp.standardize(spreadH)
    illiqH = supp.standardize(illiqH)
    global_volumesH = supp.standardize(global_volumesH)
    returnsH = supp.standardize(returnsH)
    log_rvolH = supp.standardize(log_rvolH)

    print("              -------------- DETERMINANTS OF INTRADAY BAS --------------")
    print()
    Y = spreadH

    # 6 lage benchmark
    Y, X_benchmark, hours_to_remove = rs.benchmark_hourly(Y, time_listH, hours_in_period=hours_in_period)
    X_benchmark = np.delete(X_benchmark, hours_to_remove, 0)
    Y = np.delete(Y, hours_to_remove)

    end_index = len(spreadH) # Final index for all series

    X_contemp = X_benchmark
    X_lagged = X_benchmark

    m_col = 0

    # Benchmark
    m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X_benchmark, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept)

    hours_to_remove_lagged = rs.adjust_hours_for_removal(hours_to_remove, n_hours=1)

    # Return
    X_temp = returnsH
    X_temp = np.delete(X_temp, hours_to_remove)
    X_temp = np.transpose(np.matrix(X_temp))

    X = np.append(X_benchmark, X_temp, axis=1)
    X_contemp = np.append(X_contemp, X_temp, axis=1)

    # Return lagged
    X_temp = rs.get_lagged_list(returnsH, time_listH, lag=1, hours_to_remove_prev=[])[0]
    X_temp = np.delete(X_temp, hours_to_remove_lagged)[0:-1]
    X_temp = np.transpose(np.matrix(X_temp))

    X = np.append(X_benchmark, X_temp, axis=1)
    X_lagged = np.append(X_lagged, X_temp, axis=1)

    # Volume
    X_temp = log_volumesH
    X_temp = np.delete(X_temp, hours_to_remove)
    X_temp = np.transpose(np.matrix(X_temp))

    X = np.append(X_benchmark, X_temp, axis=1)
    X_contemp = np.append(X_contemp, X_temp, axis=1)

    # Volume lagged
    X_temp = rs.get_lagged_list(log_volumesH, time_listH, lag=1, hours_to_remove_prev=[])[0]
    X_temp = np.delete(X_temp, hours_to_remove_lagged)[0:-1]
    X_temp = np.transpose(np.matrix(X_temp))

    X = np.append(X_benchmark, X_temp, axis=1)
    X_lagged = np.append(X_lagged, X_temp, axis=1)


    # Global volumes
    X_temp = global_volumesH
    X_temp = np.delete(X_temp, hours_to_remove)
    X_temp = np.transpose(np.matrix(X_temp))

    X = np.append(X_benchmark, X_temp, axis=1)
    X_contemp = np.append(X_contemp, X_temp, axis=1)

    # Global Volumes lagged
    X_temp = rs.get_lagged_list(global_volumesH, time_listH, lag=1, hours_to_remove_prev=[])[0]
    X_temp = np.delete(X_temp, hours_to_remove_lagged)[0:-1]
    X_temp = np.transpose(np.matrix(X_temp))

    X = np.append(X_benchmark, X_temp, axis=1)
    X_lagged = np.append(X_lagged, X_temp, axis=1)

    # Volatility
    X_temp = log_rvolH
    X_temp = np.delete(X_temp, hours_to_remove)
    X_temp = np.transpose(np.matrix(X_temp))

    X = np.append(X_benchmark, X_temp, axis=1)
    X_contemp = np.append(X_contemp, X_temp, axis=1)

    # Volatility lagged
    X_temp = rs.get_lagged_list(log_rvolH, time_listH, lag=1, hours_to_remove_prev=[])[0]
    X_temp = np.delete(X_temp, hours_to_remove_lagged)[0:-1]
    X_temp = np.transpose(np.matrix(X_temp))

    X = np.append(X_benchmark, X_temp, axis=1)
    X_lagged = np.append(X_lagged, X_temp, axis=1)

    # Contempraneous
    print(print_all*"                     -----------------Contemporanous---------------")
    m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X_contemp, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)

    # Lagged
    print(print_all*"                     -----------------Lagged---------------")
    m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X_lagged, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)




# Lager alt dettesom om benchmark er:
# 3 time_based, AR(1), bas^(t-24), bas^(2D)

first_col_entries = ['$bas_{t-1}$', '$bas_{t-24}$','$bas^{D}$', '$|r_t[$', '$|r_{t-1}|$', '$v_{t}$',
                     '$v_{t-1}$', '$gv_{t}$', '$gv_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']

n_rows = 3 + (len(first_col_entries)-3) * 2  # in final table
##
n_rows_to_skip = int(24/hours_in_period)  # Altså antall rader i benchmarken vi ønsker å hoppe over pga tidsbasert
n_other_entries_in_benchmark = np.size(X_benchmark,1)-n_rows_to_skip
benchmark_rows_in_print = n_other_entries_in_benchmark * 2
n_bench = benchmark_rows_in_print  #brevity
n_variables = 4
n_other_rows = n_variables * 2 * 2
##
# 11 Lage prints

first_col = []
j = 0
for i in range(0, len(first_col_entries)):
    first_col.append(first_col_entries[i])
    for k in range(len(first_col_entries[i]), 18):  # Tallet her skal være lengden på den lengste entrien (string)
        first_col[j] += ' '  # Passer på at alle blir like lange
    j += 1
    if i < (n_rows - 3) / 2:
        first_col.append('                  ')  # De første n-3 radene skal ha mellomrom mellom seg
        j += 1

print_rows = []
# Fyller starten med tomromm så det blir lettere å se
for i in range(0, n_rows):
    print_rows.append('        ')
for r in range(0, n_rows):
    print_rows[r] += (first_col[r]) + "&"

# Dette er benchmarken
for print_r in range(0, n_bench, 2):
    data_r = int(print_r/2) + n_rows_to_skip
    for c in range(0, n_cols):
        print_rows[print_r] = rs.fmt_print(print_rows[print_r], coeff_matrix[data_r, c], p_values_matrix[data_r, c], type="coeff")
        print_rows[print_r + 1] = rs.fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                               type="std_err")
    data_r += 1

# Dette er regresjonene mot en og en annen variabel
for print_r in range(n_bench, n_bench + n_other_rows, 2):
    data_r = 11
    for c in range(0, n_cols):
        if c == int(print_r / 2) - 2:
            print_rows[print_r] = rs.fmt_print(print_rows[print_r], coeff_matrix[data_r, c], p_values_matrix[data_r, c], type="coeff")
            print_rows[print_r + 1] = rs.fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c], type="std_err")
            data_r += 1
        elif c == 9 and (print_r == 6 or print_r == 10 or print_r == 14 or print_r == 18):
            i_cont = 11 + int((print_r - 6) / 4)
            print_rows[print_r] = rs.fmt_print(print_rows[print_r], coeff_matrix[i_cont, c], p_values_matrix[i_cont, c], type="coeff")
            print_rows[print_r + 1] = rs.fmt_print(print_rows[print_r + 1], std_errs_matrix[i_cont, c], type="std_err")
        elif c == 10 and (print_r == 8 or print_r == 12 or print_r == 16 or print_r == 20):
            i_lag = 11 + int((print_r - 8) / 4)
            print_rows[print_r] = rs.fmt_print(print_rows[print_r], coeff_matrix[i_lag, c],
                                               p_values_matrix[i_lag, c], type="coeff")
            print_rows[print_r + 1] = rs.fmt_print(print_rows[print_r + 1], std_errs_matrix[i_lag, c],
                                                   type="std_err")
        else:
            print_rows[print_r] += "           &"
            print_rows[print_r + 1] += "           &"

# Dette fikser de tre nedreste radene
print_rows = rs.final_three_rows(print_rows, n_obs_array, rsquared_array, aic_array, n_cols, n_rows)

print()
print("         ----------------------------------------------------", str(exc_name), "---------------------------------------------")
rs.final_print_regressions_latex(print_rows)  # Gjør hele printejobben
