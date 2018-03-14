import numpy as np
from inspect import currentframe, getframeinfo
import data_import as di
import data_import_support as dis
from Sondre import sondre_support_formulas as supp
from Jacob import jacob_support as jake_supp

# 1 kontrollpanel
log_illiqs = 1 # Should log-illiq be used rather than plain illiq?
hours_in_period = 4 # 1, 2, 3, or 4 hours in dummies
benchmark_only = 1 # For testing

spread_determinants = 1  # perform analysis on determinants of spread
illiq_determinants = 0  # perform analysis on determinants of illiq    IKKE LAGET ENDA
return_determinants = 0  # perform analysis on determinants of return  IKKE LAGET ENDA


# 2 importere prices, volumes
#exchange_list, time_listM, pricesM, volumesM = di.get_lists(opening_hours="n", make_totals="n")
exchange_list = ["TEST"]
exchanges = [0]  # just for testing

# 3 iterere over exchanges
for exc in exchanges:
    print("Intraday determinants regression for", exchange_list[exc].upper())
    print()
    # 4 importere clean_trans_hours
    #time_listH, returnsH, spreadH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_trans_hours(time_listM, pricesM, volumesM, exc=exc)
    time_listH = ['01.01.2012 00:00', '01.01.2012 01:00', '01.01.2012 02:00', '01.01.2012 03:00', '01.01.2012 04:00',
                 '01.01.2012 05:00', '01.01.2012 06:00', '01.01.2012 07:00', '01.01.2012 08:00', '01.01.2012 09:00',
                 '01.01.2012 10:00', '01.01.2012 11:00', '01.01.2012 12:00', '01.01.2012 13:00', '01.01.2012 14:00',
                 '01.01.2012 15:00', '01.01.2012 16:00', '01.01.2012 17:00', '01.01.2012 18:00', '01.01.2012 19:00',
                 '01.01.2012 20:00', '01.01.2012 21:00', '01.01.2012 22:00', '01.01.2012 23:00', '02.01.2012 00:00',
                 '02.01.2012 01:00', '02.01.2012 02:00', '02.01.2012 03:00', '02.01.2012 04:00', '02.01.2012 05:00',
                 '02.01.2012 06:00', '02.01.2012 07:00', '02.01.2012 08:00', '02.01.2012 09:00', '02.01.2012 10:00',
                 '02.01.2012 11:00', '02.01.2012 12:00', '02.01.2012 13:00', '02.01.2012 14:00', '02.01.2012 15:00',
                 '02.01.2012 16:00', '02.01.2012 17:00', '02.01.2012 18:00', '02.01.2012 19:00', '02.01.2012 20:00',
                 '02.01.2012 21:00', '02.01.2012 22:00', '02.01.2012 23:00']
    pricesH = [0.1, 0.7, 1.8, 3.4, 4.4, 4.8, 6.0, 7.1, 7.9, 8.7, 10.4, 10.8, 12.5, 12.6, 13.7, 15.1, 16.2, 16.6, 18.0,
            18.6, 19.9, 20.5, 22.4, 23.2, 23.8, 25.3, 25.7, 26.8, 28.0, 29.5, 30.1, 30.8, 32.2, 32.9, 34.2, 34.6, 36.4,
            36.8, 38.0, 39.1, 39.6, 40.7, 42.2, 43.4, 44.3, 45.1, 45.8, 47.1]
    returnsH = jake_supp.logreturn(pricesH)
    spreadH = pricesH
    log_illiqH = returnsH
    log_rvolH = returnsH
    log_volumesH = pricesH

    if log_illiqs:
        illiqH = log_illiqH

    # 5 standardisere
    print(" Standardizing all series")
    print()
    log_volumesH = supp.standardize(log_volumesH)
    spreadH = supp.standardize(spreadH)
    illiqH = supp.standardize(illiqH)
    returnsH = supp.standardize(returnsH)
    log_rvolH = supp.standardize(log_rvolH)

    if spread_determinants == 1:
        print(" DETERMINANTS OF INTRADAY BAS-------------------")
        Y = spreadH
        end_index = len(spreadH) # Final index for all series
        n_cols = 10  # 10 for BAS og for ILLIQ

        # 6 lage benchmark
        Y, X_benchmark, max_lag = supp.benchmark_hourly(Y, time_listH, HAR_config=0, hours_in_period=hours_in_period)
        line_nr = getframeinfo(currentframe()).lineno + 1

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
        print(" %i: Length of Y is %i and  X_benchmark is (%i,%i)" % (getframeinfo(currentframe()).lineno, len(Y), np.size(X_benchmark, 0), np.size(X_benchmark, 1)))
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X_benchmark, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, prints=benchmark_only)

        if benchmark_only == 0:
            # Return
            X_temp = returnsH[max_lag:end_index]
            X_temp = np.transpose(np.matrix(X_temp))

            X = np.append(X_benchmark, X_temp, axis=1)
            X_contemp = np.append(X_contemp, X_temp, axis=1)
            print(" %i: Length of Y is %i and  X_benchmark is (%i,%i) while X_temp is (%i,%i) and x_contemp is (%i,%i) and x_lagged is (%i,%i)" % (getframeinfo(currentframe()).lineno, len(Y), np.size(X_benchmark, 0), np.size(X_benchmark, 1), np.size(X_temp, 0), np.size(X_temp, 1), np.size(X_contemp, 0), np.size(X_contemp, 1), np.size(X_lagged, 0), np.size(X_lagged,1)))

            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,n_obs_array)

            # Return lagged
            X_temp = returnsH[max_lag - 1:end_index - 1]
            X_temp = np.transpose(np.matrix(X_temp))

            X = np.append(X_benchmark, X_temp, axis=1)
            X_lagged = np.append(X_lagged, X_temp, axis=1)

            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Volume
            X_temp = log_volumesH[max_lag:end_index]
            X_temp = np.transpose(np.matrix(X_temp))

            X = np.append(X_benchmark, X_temp, axis=1)
            X_contemp = np.append(X_contemp, X_temp, axis=1)

            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Volume lagged
            X_temp = log_volumesH[max_lag - 1:end_index - 1]
            X_temp = np.transpose(np.matrix(X_temp))

            X = np.append(X_benchmark, X_temp, axis=1)
            X_lagged = np.append(X_lagged, X_temp, axis=1)

            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Volatility
            X_temp = log_rvolH[max_lag:end_index]
            X_temp = np.transpose(np.matrix(X_temp))

            X = np.append(X_benchmark, X_temp, axis=1)
            X_contemp = np.append(X_contemp, X_temp, axis=1)

            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,n_obs_array)

            # Volatility lagged
            X_temp = log_rvolH[max_lag - 1:end_index - 1]
            X_temp = np.transpose(np.matrix(X_temp))

            X = np.append(X_benchmark, X_temp, axis=1)
            X_lagged = np.append(X_lagged, X_temp, axis=1)
            print(" %i: Length of Y is %i and  X_benchmark is (%i,%i) while X_temp is (%i,%i) and x_contemp is (%i,%i) and x_lagged is (%i,%i)" % (getframeinfo(currentframe()).lineno, len(Y), np.size(X_benchmark, 0), np.size(X_benchmark, 1), np.size(X_temp, 0), np.size(X_temp, 1), np.size(X_contemp, 0), np.size(X_contemp, 1), np.size(X_lagged, 0), np.size(X_lagged,1)))

            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,n_obs_array)

            # Contempraneous
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X_contemp, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Lagged
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = supp.import_regressions(m_col, Y, X_lagged, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            first_col_entries = ['Intercept', '$bas^D$', '$bas^W$', '$bas^{2M}$', '$r_t$', '$r_{t-1}$', '$v_{t}$',
                                 '$v_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']


        # 11 Lage prints
        # 12 printe til latex


