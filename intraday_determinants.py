import numpy as np
from inspect import currentframe, getframeinfo
from matplotlib import pyplot as plt
import data_import
import data_import as di
import data_import_support as dis
import legacy
import regression_support
from Sondre import sondre_support_formulas as supp
from Jacob import jacob_support as jake_supp

# 1 kontrollpanel
log_illiqs = 1 # Should log-illiq be used rather than plain illiq?
hours_in_period = 8 # 2, 3 or 4 hours in dummies
standardized_coeffs = 0 # Should be 1

benchmark_only = 1  # For testing
bench_types = [1, 2, 3, 4, 5]
benchmark_prints = 1  # For kontroll av antall rader og kolonner
intercept = 0
force_max_lag = benchmark_only * 48  # Når vi vil sammenlikne benchmarks


spread_determinants = 1  # perform analysis on determinants of spread
illiq_determinants = 0  # perform analysis on determinants of illiq    IKKE LAGET ENDA
return_determinants = 0  # perform analysis on determinants of return  IKKE LAGET ENDA


# 2 importere prices, volumes
exchanges = [0, 1, 2, 3]
exchanges = [0]  # just for testing

# 3 iterere over exchanges

for exc in exchanges:
    exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = di.get_list(exc=exc, freq='h', local_time=1)

    supp.print_n(50)
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
            n_cols = 10  # 10 for BAS og for ILLIQ

            # 6 lage benchmark
            Y, X_benchmark, max_lag = regression_support.benchmark_hourly(Y, time_listH, HAR_config=bench_type, hours_in_period=hours_in_period, prints=benchmark_prints, force_max_lag=force_max_lag)

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
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(m_col, Y, X_benchmark, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, prints=benchmark_prints, intercept=intercept)
            #supp.print_n(max(0, 35 - np.size(coeff_matrix, 1)-bench_type))


            if benchmark_only != 1:
                # Return
                X_temp = returnsH[max_lag:end_index]
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

                # Return lagged
                X_temp = returnsH[max_lag - 1:end_index - 1]
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)

                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

                # Volume
                X_temp = log_volumesH[max_lag:end_index]
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

                # Volume lagged
                X_temp = log_volumesH[max_lag - 1:end_index - 1]
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)

                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

                # Volatility
                X_temp = log_rvolH[max_lag:end_index]
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_contemp = np.append(X_contemp, X_temp, axis=1)

                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

                # Volatility lagged
                X_temp = log_rvolH[max_lag - 1:end_index - 1]
                X_temp = np.transpose(np.matrix(X_temp))

                X = np.append(X_benchmark, X_temp, axis=1)
                X_lagged = np.append(X_lagged, X_temp, axis=1)

                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,n_obs_array)

                # Contempraneous
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(m_col, Y, X_contemp, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, prints=1)

                # Lagged
                m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(m_col, Y, X_lagged, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, prints=1)

                first_col_entries = ['Intercept', '$bas^D$', '$bas^W$', '$bas^{2M}$', '$r_t$', '$r_{t-1}$', '$v_{t}$',
                                     '$v_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']




                # 11 Lage prints
                # 12 printe til latex


