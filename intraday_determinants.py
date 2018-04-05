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

# 1 kontrollpanel
log_illiqs = 0 # Should log-illiq be used rather than plain illiq?
hours_in_period = 3 # 2, 3 or 4 hours in dummies
standardized_coeffs = 1 # Should be 1

benchmark_only = 0  # For testing
bench_types = [3]
print_all = 0
benchmark_prints = 0  # For kontroll av antall rader og kolonner
intercept = 0
force_max_lag = benchmark_only * 48  # Når vi vil sammenlikne benchmarks


spread_determinants = 1  # perform analysis on determinants of spread
illiq_determinants = 0  # perform analysis on determinants of illiq    IKKE LAGET ENDA
return_determinants = 0  # perform analysis on determinants of return  IKKE LAGET ENDA

# 2 importere prices, volumes
exchanges = [0, 2, 3, 4]

# 3 iterere over exchanges

for exc in exchanges:
    exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = di.get_list(exc=exc, freq='h', local_time=1)

    #supp.print_n(50)
    print("----------------- INTRADAY DETERMINANTS REGRESSION FOR", exc_name.upper()[0:-3], "----------------------")
    force_max_lag = 48
    for bench_type in bench_types:
        print("     ---------------------------- Configuration %i ----------------------------" % bench_type)
        if hours_in_period != -1:
            print("     --------------------------- %i hours per period --------------------------" % hours_in_period)

        print()

        if log_illiqs == 1:
            illiqH = log_illiqH

        if standardized_coeffs == 1:
            print(" Standardizing all series")
            print()
            log_volumesH = supp.standardize(log_volumesH)
            spreadH = supp.standardize(spreadH)
            illiqH = supp.standardize(illiqH)
            returnsH = supp.standardize(returnsH)
            log_rvolH = supp.standardize(log_rvolH)

        if spread_determinants == 1:
            print("              -------------- DETERMINANTS OF INTRADAY BAS --------------")
            print()
            Y = spreadH
            n_cols = 9  # 10 for BAS og for ILLIQ

            # 6 lage benchmark
            Y, X_benchmark, max_lag, hours_to_remove = rs.benchmark_hourly(Y, time_listH, HAR_config=bench_type, hours_in_period=hours_in_period, prints=benchmark_prints, force_max_lag=force_max_lag)

            print("   \033[32;0;0mintday_dets.%i: Length of Y %i\033[0;0;0m" % (gf(cf()).lineno, len(Y)))
            print("   \033[32;0;0mintday_dets.%i: Size of benchmark: (%i,%i)\033[0;0;0m" % (gf(cf()).lineno, np.size(X_benchmark,0), np.size(X_benchmark,1)))
            print("   \033[32;0;0mintday_dets.%i: Number of hours removed: %i\033[0;0;0m" % (gf(cf()).lineno, len(hours_to_remove)))
            X_benchmark = np.delete(X_benchmark, hours_to_remove, 0)
            Y = np.delete(Y, hours_to_remove)
            print("   \033[32;0;0mintday_dets.%i: Length of Y %i\033[0;0;0m" % (gf(cf()).lineno, len(Y)))
            print("   \033[32;0;0mintday_dets.%i: Size of benchmark: (%i,%i)\033[0;0;0m" % (gf(cf()).lineno, np.size(X_benchmark,0), np.size(X_benchmark,1)))

            end_index = len(spreadH) # Final index for all series

            n_entries = np.size(X_benchmark, 0)
            coeff_matrix = np.zeros([n_entries, n_cols])
            rsquared_array = np.zeros(n_cols)
            aic_array = np.zeros(n_cols)
            n_obs_array = np.zeros(n_cols)
            p_values_matrix = np.zeros([n_entries, n_cols])
            std_errs_matrix = np.zeros([n_entries, n_cols])

            X_contemp = X_benchmark
            X_lagged = X_benchmark

            """
            #print("The determinant of the benchmark is: ",np.linalg.det(X_benchmark))
            time_listH = time_listH[max_lag:]
            print("                   0   3   6   9   12  15  18  21")
            for i in range(20):
                print(time_listH[i], end="   ")
                for j in range(8):
                    print(int(X_benchmark[i, j]), end="   ")
                print()
            """
            m_col = 0

            # Benchmark
            print(benchmark_prints * "                     -----------------Benchmark---------------")
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X_benchmark, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, prints=benchmark_prints, intercept=intercept)
            #supp.print_n(max(0, 35 - np.size(coeff_matrix, 1)-bench_type))

            if benchmark_only != 1:
                # Return
                ############
                # Må finne en måte å hente lagged, nå som max_lag ikke er verdt shit.
                ##############
                X_temp = returnsH[]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                print(print_all*"                     -----------------Returns---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)

                # Return lagged
                X_temp = returnsH[max_lag - 1:- 1]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)
                print(print_all*"                     -----------------Returns lagged---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)

                # Volume
                X_temp = log_volumesH[max_lag:]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                print(print_all*"                     -----------------Volumes---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)

                # Volume lagged
                X_temp = log_volumesH[max_lag - 1:-1]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)

                print(print_all*"                     -----------------Volumes lagged---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)

                # Volatility
                X_temp = log_rvolH[max_lag:]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                print(print_all*"                     -----------------Volatility---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)

                # Volatility lagged
                X_temp = log_rvolH[max_lag - 1:-1]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)

                print(print_all*"                     -----------------Volatility lagged---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,n_obs_array, intercept=intercept, prints=print_all)

                # Contempraneous
                print(print_all*"                     -----------------Contemporanous---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X_contemp, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)

                # Lagged
                print(print_all*"                     -----------------Lagged---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(m_col, Y, X_lagged, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=intercept, prints=print_all)




                # Lager alt dettesom om benchmark er:
                # 3 time_based, AR(1), bas^(t-24), bas^(2D)

                first_col_entries = ['$AR(1)$', '$bas^{t-24}$','$bas^{D}$', '$r_t$', '$r_{t-1}$', '$v_{t}$',
                                     '$v_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']

                n_rows = 3 + (len(first_col_entries)-3) * 2  # in final table
                ##
                n_rows_to_skip = int(24/hours_in_period)  # Altså antall rader i benchmarken vi ønsker å hoppe over pga tidsbasert
                n_other_entries_in_benchmark = np.size(X_benchmark,1)-n_rows_to_skip
                benchmark_rows_in_print = n_other_entries_in_benchmark * 2
                n_bench = benchmark_rows_in_print  #brevity
                n_variables = 3
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
                        elif c == 7 and (print_r == 6 or print_r == 10 or print_r == 14 or print_r == 18):
                            i_cont = 11 + int((print_r - 6) / 4)
                            print_rows[print_r] = rs.fmt_print(print_rows[print_r], coeff_matrix[i_cont, c], p_values_matrix[i_cont, c], type="coeff")
                            print_rows[print_r + 1] = rs.fmt_print(print_rows[print_r + 1], std_errs_matrix[i_cont, c], type="std_err")
                        elif c == 8 and (print_r == 8 or print_r == 12 or print_r == 16 or print_r == 20):
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

                # 12 printe til latex

        if illiq_determinants == 1:
            print("              -------------- DETERMINANTS OF INTRADAY ILLIQ --------------")
            print()
            Y = illiqH
            n_cols = 9

            # 6 lage benchmark
            Y, X_benchmark, max_lag, hours_to_remove = rs.benchmark_hourly(Y, time_listH, HAR_config=bench_type,
                                                                           hours_in_period=hours_in_period,
                                                                           prints=benchmark_prints,
                                                                           force_max_lag=force_max_lag)

            print("   \033[32;0;0mintday_dets.%i: Number of hours removed: %i\033[0;0;0m" % (
            gf(cf()).lineno, len(hours_to_remove)))
            X_benchmark = np.delete(X_benchmark, hours_to_remove, 0)
            Y = Y[max_lag:]
            Y = np.delete(Y, hours_to_remove)

            end_index = len(illiqH)  # Final index for all series

            n_entries = np.size(X_benchmark, 0)
            coeff_matrix = np.zeros([n_entries, n_cols])
            rsquared_array = np.zeros(n_cols)
            aic_array = np.zeros(n_cols)
            n_obs_array = np.zeros(n_cols)
            p_values_matrix = np.zeros([n_entries, n_cols])
            std_errs_matrix = np.zeros([n_entries, n_cols])

            X_contemp = X_benchmark
            X_lagged = X_benchmark

            m_col = 0

            # Benchmark
            print(benchmark_prints * "                     -----------------Benchmark---------------")
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                m_col, Y, X_benchmark, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                n_obs_array, prints=benchmark_prints, intercept=intercept)
            # supp.print_n(max(0, 35 - np.size(coeff_matrix, 1)-bench_type))


            if benchmark_only != 1:
                # Return
                X_temp = returnsH[max_lag:]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                print(print_all * "                     -----------------Returns---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                    intercept=intercept, prints=print_all)

                # Return lagged
                X_temp = returnsH[max_lag - 1:- 1]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)
                print(print_all * "                     -----------------Returns lagged---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                    intercept=intercept, prints=print_all)

                # Volume
                X_temp = log_volumesH[max_lag:]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                print(print_all * "                     -----------------Volumes---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                    intercept=intercept, prints=print_all)

                # Volume lagged
                X_temp = log_volumesH[max_lag - 1:-1]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)

                print(print_all * "                     -----------------Volumes lagged---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                    intercept=intercept, prints=print_all)

                # Volatility
                X_temp = log_rvolH[max_lag:]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                print(print_all * "                     -----------------Volatility---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                    intercept=intercept, prints=print_all)

                # Volatility lagged
                X_temp = log_rvolH[max_lag - 1:-1]
                X_temp = np.delete(X_temp, hours_to_remove)
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)

                print(print_all * "                     -----------------Volatility lagged---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                    m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                    intercept=intercept, prints=print_all)

                # Contempraneous
                print(print_all * "                     -----------------Contemporanous---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                    m_col, Y, X_contemp, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                    n_obs_array, intercept=intercept, prints=print_all)

                # Lagged
                print(print_all * "                     -----------------Lagged---------------")
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = rs.import_regressions(
                    m_col, Y, X_lagged, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                    n_obs_array, intercept=intercept, prints=print_all)

                # Lager alt dettesom om benchmark er:
                # 3 time_based, AR(1), bas^(t-24), bas^(2D)

                first_col_entries = ['$AR(1)$', '$illiq^{t-24}$', '$illiq^{D}$', '$r_t$', '$r_{t-1}$', '$v_{t}$',
                                     '$v_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$',
                                     '\\textit{AIC}']

                n_rows = 3 + (len(first_col_entries) - 3) * 2  # in final table
                ##
                n_rows_to_skip = int(
                    24 / hours_in_period)  # Altså antall rader i benchmarken vi ønsker å hoppe over pga tidsbasert
                n_other_entries_in_benchmark = np.size(X_benchmark, 1) - n_rows_to_skip
                benchmark_rows_in_print = n_other_entries_in_benchmark * 2
                n_bench = benchmark_rows_in_print  # brevity
                n_variables = 3
                n_other_rows = n_variables * 2 * 2
                ##
                # 11 Lage prints

                first_col = []
                j = 0
                for i in range(0, len(first_col_entries)):
                    first_col.append(first_col_entries[i])
                    for k in range(len(first_col_entries[i]),
                                   18):  # Tallet her skal være lengden på den lengste entrien (string)
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
                    data_r = int(print_r / 2) + n_rows_to_skip
                    for c in range(0, n_cols):
                        print_rows[print_r] = rs.fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                           p_values_matrix[data_r, c], type="coeff")
                        print_rows[print_r + 1] = rs.fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                                               type="std_err")
                    data_r += 1

                # Dette er regresjonene mot en og en annen variabel
                for print_r in range(n_bench, n_bench + n_other_rows, 2):
                    data_r = 11
                    for c in range(0, n_cols):
                        if c == int(print_r / 2) - 2:
                            print_rows[print_r] = rs.fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                               p_values_matrix[data_r, c], type="coeff")
                            print_rows[print_r + 1] = rs.fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                                                   type="std_err")
                            data_r += 1
                        elif c == 7 and (print_r == 6 or print_r == 10 or print_r == 14 or print_r == 18):
                            i_cont = 11 + int((print_r - 6) / 4)
                            print_rows[print_r] = rs.fmt_print(print_rows[print_r], coeff_matrix[i_cont, c],
                                                               p_values_matrix[i_cont, c], type="coeff")
                            print_rows[print_r + 1] = rs.fmt_print(print_rows[print_r + 1], std_errs_matrix[i_cont, c],
                                                                   type="std_err")
                        elif c == 8 and (print_r == 8 or print_r == 12 or print_r == 16 or print_r == 20):
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
                print("         ----------------------------------------------------", str(exc_name),
                      "---------------------------------------------")
                rs.final_print_regressions_latex(print_rows)  # Gjør hele printejobben

                # 12 printe til latex
