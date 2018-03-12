import os

import numpy as np

import data_import as di
import data_import_support as dis
import linreg
from Sondre import sondre_support_formulas as supp
from Sondre.sondre_support_formulas import import_to_matrices, print_n, \
    import_regressions, fmt_print

os.chdir("/Users/sondre/Documents/GitHub/krypto")

exch = [1]  # 0=bitstamp, 1=coincheck

intraweek_pattern_regression = 1
subtract_means = 1  # from day-of-week regression
convert_coeffs_to_percentage = 1
convert_logs = 0
log_illiqs = True

determinants_regression = 1
autoreg = 0

rolls_multi = 1
illiq_multi = 1
return_multi = 1

exchanges, time_list_minutes, prices_minutes, volumes_minutes = di.get_lists(opening_hours="n", make_totals="n")

for exc in exch:
    time_list_days, time_list_removed, returns_days, volumes_days, log_volumes_days, spread_days, illiq_days, log_illiq_days, rvol_days, log_rvol_days = \
        dis.clean_trans_days(time_list_minutes, prices_minutes, volumes_minutes, exc=exc, print_days_excluded=0, convert_time_zones=1)

    if log_illiqs:
        illiq = log_illiq_days
    else:
        illiq = illiq_days

    if determinants_regression == 1:
        stdzd_log_volumes_days = supp.standardize(log_volumes_days)
        stdzd_spread_days = supp.standardize(spread_days)
        stdzd_illiq_days = supp.standardize(illiq)
        stdzd_returns_days = supp.standardize(returns_days)
        stdzd_log_rvol_days = supp.standardize(log_rvol_days)

    print()
    print()
    print()
    print("     ------------------------------------------------", str(exchanges[exc]),
          "-----------------------------------------")
    print()

    mon, tue, wed, thu, fri, sat, sun = supp.week_vars(time_list_days)
    weekend = np.zeros(len(mon))
    for data_r in range(0, len(mon)):
        if sat[data_r] + sun[data_r] > 0:
            weekend[data_r] = 1

    if intraweek_pattern_regression == 1:  # Er ikke oppdatert med ny output!
        X = np.matrix(mon)
        X = np.append(X, np.matrix(tue), axis=0)
        X = np.append(X, np.matrix(wed), axis=0)
        X = np.append(X, np.matrix(thu), axis=0)
        X = np.append(X, np.matrix(fri), axis=0)
        X = np.append(X, np.matrix(sat), axis=0)
        X = np.append(X, np.matrix(sun), axis=0)
        X = np.transpose(X)

        n_rows = 21  # in final table
        n_cols = 10
        n_entries = 7  # Må bare være minst like stor som antall forklaringsvariable
        coeff_matrix = np.zeros([n_entries, n_cols])
        rsquared_array = np.zeros(n_cols)
        aic_array = np.zeros(n_cols)
        n_obs_array = np.zeros(n_cols)
        p_values_matrix = np.zeros([n_entries, n_cols])
        std_errs_matrix = np.zeros([n_entries, n_cols])

        m_col = 0  # Må bare intitialiseres til null, også nar "import_reg" seg av å oppdatere den

        Y = returns_days
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
            intercept=0)
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        Y = log_volumes_days
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
            intercept=0)
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
            prints=0)

        Y = log_rvol_days
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
            intercept=0)
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        Y = spread_days
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
            intercept=0)
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        Y = illiq
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
            intercept=0)
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
            m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

        if subtract_means == 1:  # Turns analysis into deviation from mean
            # Now we need to subtract the means from the coefficient matrix

            returns_days -= np.mean(coeff_matrix[:, 0])
            log_volumes_days -= np.mean(coeff_matrix[:, 2])
            log_rvol_days -= np.mean(coeff_matrix[:, 4])
            spread_days -= np.mean(coeff_matrix[:, 6])
            illiq -= np.mean(coeff_matrix[:, 8])

            coeff_matrix = np.zeros([n_entries, n_cols])
            rsquared_array = np.zeros(n_cols)
            aic_array = np.zeros(n_cols)
            n_obs_array = np.zeros(n_cols)
            p_values_matrix = np.zeros([n_entries, n_cols])
            std_errs_matrix = np.zeros([n_entries, n_cols])

            m_col = 0  # Må bare intitialiseres til null, også nar "import_reg" seg av å oppdatere den

            Y = returns_days
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0)
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                n_obs_array)

            Y = log_volumes_days
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0)
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                n_obs_array,
                prints=0)

            Y = log_rvol_days
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0)
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                n_obs_array)

            Y = spread_days
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0)
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                n_obs_array)
            Y = illiq
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0)
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = import_regressions(
                m_col, Y, weekend, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                n_obs_array)

        if convert_coeffs_to_percentage == 1:
            print()
            print()
            print()
            print("NB!! Converting returnsH and spreadH back into percentage")
            for c in [0, 1, 6, 7]:  # 0-1=returnsH 6-7=spreadH
                for i in range(0, n_entries):
                    coeff_matrix[i, c] = 100 * coeff_matrix[i, c]
                    std_errs_matrix[i, c] = 100 * std_errs_matrix[i, c]
            if convert_logs == 1:  # This logic is not sound. e^(error) does not make sense
                print("NB!! Converting rvol and illiq back into percentage")
                for c in [4, 5, 8, 9]:  # 4-5=rvol 8-9=illiq
                    for i in range(0, n_entries):
                        coeff_matrix[i, c] = 100 * np.exp(coeff_matrix[i, c])
                        std_errs_matrix[i, c] = 100 * np.exp(std_errs_matrix[i, c])

        first_col_entries = ['\\textit{Mon}', '\\textit{Tue}', '\\textit{Wed}', '\\textit{Thu}', '\\textit{Fri}',
                             '\\textit{Sat}', '\\textit{Sun}', '\\textit{Weekday}', '\\textit{Weekend}',
                             '\\textit{\\# Obs.}', '$R^2$',
                             '\\textit{AIC}']

        first_col = []
        j = 0

        for i in range(0, len(first_col_entries)):
            first_col.append(first_col_entries[i])
            for k in range(len(first_col_entries[i]), 18):  # Tallet her skal være lengden på den lengste entrien
                first_col[j] += ' '  # Passer på at alle blir like lange
            j += 1
            if i < 9:
                first_col.append('                  ')  # De første 9 radene skal ha mellomrom mellom seg
                j += 1

        print()
        data_r = 0
        print_rows = []

        # Fyller starten med tomromm så det blir lettere å se
        for k in range(0, n_rows):
            print_rows.append('        ')
        for print_r in range(0, n_rows):
            print_rows[print_r] += (first_col[print_r]) + "&"

        for print_r in range(0, 14, 2):
            for c in range(0, n_cols, 2):
                print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                p_values_matrix[data_r, c],
                                                type="coeff")
                print_rows[print_r] += "          & &"
                print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c], type="std_err")
                print_rows[print_r + 1] += "          & &"
            data_r += 1

        data_r = 0
        for print_r in [14, 16]:
            print_rows[print_r] += "           &"
            print_rows[print_r + 1] += "           &"

            for c in range(1, n_cols, 2):
                print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                p_values_matrix[data_r, c],
                                                type="coeff")
                print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c], type="std_err")
                if c < n_cols - 1:
                    print_rows[print_r] += " &          &"
                    print_rows[print_r + 1] += " &          &"
                else:
                    print_rows[print_r] += "      "
                    print_rows[print_r + 1] += "       "

            data_r += 1

        # Dette fikser de tre nedreste radene
        print_rows = supp.final_three_rows(print_rows, n_obs_array, rsquared_array, aic_array, n_cols, n_rows,
                                           double_cols=1)

        print(
            "     ------------------------------------------------Regression table for Intraweek seasonality-----------------------------------------")
        print()
        print()
        supp.final_print_regressions_latex(print_rows)  # Gjør hele printejobben

    if determinants_regression == 1:

        # Fetch the standardized variables from earlier
        log_volumes_days = stdzd_log_volumes_days
        spread_days = stdzd_spread_days
        illiq = stdzd_illiq_days
        returns_days = stdzd_returns_days
        log_rvol_days = stdzd_log_rvol_days

        lags = [1, 7, 60]
        max_lag = 60  # Locked
        n_lags = len(lags)

        weekend = np.matrix(weekend[max_lag: len(spread_days)])
        weekend = np.transpose(weekend)
        mon = np.matrix(mon[max_lag: len(spread_days)])
        mon = np.transpose(mon)
        tue = np.matrix(tue[max_lag: len(spread_days)])
        tue = np.transpose(tue)
        wed = np.matrix(wed[max_lag: len(spread_days)])
        wed = np.transpose(wed)
        thu = np.matrix(thu[max_lag: len(spread_days)])
        thu = np.transpose(thu)
        fri = np.matrix(fri[max_lag: len(spread_days)])
        fri = np.transpose(fri)
        sat = np.matrix(sat[max_lag: len(spread_days)])
        sat = np.transpose(sat)
        sun = np.matrix(sun[max_lag: len(spread_days)])
        sun = np.transpose(sun)

        if rolls_multi == 1:
            Y = spread_days[max_lag: len(spread_days)]
            n_days = len(Y)
            start_index = len(spread_days) - n_days
            end_index = len(spread_days)
            X = []

            for j in range(n_lags):
                # print("x%i: BAS with %i days lag" % (j + 1, lags[j]))
                x = supp.mean_for_n_entries(spread_days, lags[j])
                x = np.matrix(x[len(x) - n_days: len(x)])
                if j == 0:
                    X = x
                else:
                    X = np.append(X, x, axis=0)

            X_benchmark = np.transpose(X)  # Har model

            X_benchmark = np.append(X_benchmark, mon, axis=1)
            X_benchmark = np.append(X_benchmark, tue, axis=1)
            X_benchmark = np.append(X_benchmark, wed, axis=1)
            X_benchmark = np.append(X_benchmark, thu, axis=1)
            X_benchmark = np.append(X_benchmark, fri, axis=1)
            X_benchmark = np.append(X_benchmark, sat, axis=1)
            X_benchmark = np.append(X_benchmark, sun, axis=1)

            X_contemporary = X_benchmark
            X_lagged = X_benchmark

            # These tables are 23 rows tall, 9 wide
            n_rows = 23  # in final table
            n_entries = 15  # Må bare være minst like stor
            n_cols = 9
            coeff_matrix = np.zeros([n_entries, n_cols])
            rsquared_array = np.zeros(n_cols)
            aic_array = np.zeros(n_cols)
            n_obs_array = np.zeros(n_cols)
            p_values_matrix = np.zeros([n_entries, n_cols])
            std_errs_matrix = np.zeros([n_entries, n_cols])

            m_col = 0
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_benchmark, prints=0)
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Spread - Return
            x = returns_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)

            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Spread - Return with 1 lag
            x = returns_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Spread - Volume
            x = log_volumes_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Spread - Volume with lag
            x = log_volumes_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Spread - Volatility
            x = log_rvol_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Spread - Volatility with lag
            x = log_rvol_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Contemporaneous
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_contemporary, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Lagged variables
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_lagged, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            first_col_entries = ['Intercept', '$bas^D$', '$bas^W$', '$bas^{2M}$', '$r_t$', '$r_{t-1}$', '$v_{t}$',
                                 '$v_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']

            first_col = []
            j = 0
            for data_r in range(0, len(first_col_entries)):
                first_col.append(first_col_entries[data_r])
                for k in range(len(first_col_entries[data_r]),
                               18):  # Tallet her skal være lengden på den lengste entrien
                    first_col[j] += ' '  # Passer på at alle blir like lange
                j += 1
                if data_r < 10:
                    first_col.append('                  ')  # De første 10 radene skal ha mellomrom mellom seg
                    j += 1

            print_rows = []
            # Fyller starten med tomromm så det blir lettere å se
            for data_r in range(0, n_rows):
                print_rows.append('        ')
            for print_r in range(0, n_rows):
                print_rows[print_r] += (first_col[print_r]) + "&"

            # Dette er benchmarken
            data_r = 0
            for print_r in range(0, 8, 2):
                for c in range(0, n_cols):
                    print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                    p_values_matrix[data_r, c], type="coeff")
                    print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                                        type="std_err")
                data_r += 1

            # Dette er regresjonene mot en og en annen variabel
            for print_r in range(8, 20, 2):
                data_r = 11
                for c in range(0, n_cols):
                    if c == int(print_r / 2) - 3:
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                        p_values_matrix[data_r, c], type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                                            type="std_err")
                        data_r += 1
                    elif c == 7 and (print_r == 8 or print_r == 12 or print_r == 16):
                        i_cont = 11 + int((print_r - 8) / 4)
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[i_cont, c],
                                                        p_values_matrix[i_cont, c],
                                                        type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[i_cont, c],
                                                            type="std_err")
                    elif c == 8 and (print_r == 10 or print_r == 14 or print_r == 18):
                        i_lag = 11 + int((print_r - 10) / 4)
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[i_cont, c],
                                                        p_values_matrix[i_cont, c],
                                                        type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[i_lag, c],
                                                            type="std_err")
                    else:
                        print_rows[print_r] += "           &"
                        print_rows[print_r + 1] += "           &"

            # Dette fikser de tre nedreste radene
            print_rows = supp.final_three_rows(print_rows, n_obs_array, rsquared_array, aic_array, n_cols, n_rows)

            print()
            print()
            print()
            print(
                "           -----------------------------------------Regression table for Bid-ask spreadH----------------------------------------")
            print()
            print()
            supp.final_print_regressions_latex(print_rows)  # Gjør hele printejobben

        if illiq_multi == 1:
            Y = illiq[max_lag: len(illiq)]
            n_entries = len(Y)
            start_index = len(illiq) - n_entries
            end_index = len(illiq)
            X = []

            # print("ILLIQ")
            # print("----------------------------------------------------------------------------------------------------------------------------")
            # print("----------------------------------------------------------------------------------------------------------------------------")

            for j in range(n_lags):
                x = supp.mean_for_n_entries(illiq, lags[j])
                x = np.matrix(x[len(x) - n_entries: len(x)])
                if j == 0:
                    X = x
                else:
                    X = np.append(X, x, axis=0)

            X_benchmark = np.transpose(X)  # Har model

            X_benchmark = np.append(X_benchmark, mon, axis=1)
            X_benchmark = np.append(X_benchmark, tue, axis=1)
            X_benchmark = np.append(X_benchmark, wed, axis=1)
            X_benchmark = np.append(X_benchmark, thu, axis=1)
            X_benchmark = np.append(X_benchmark, fri, axis=1)
            X_benchmark = np.append(X_benchmark, sat, axis=1)
            X_benchmark = np.append(X_benchmark, sun, axis=1)

            X_contemporary = X_benchmark
            X_lagged = X_benchmark

            # These tables are 23 rows tall, 9 wide
            n_rows = 23  # in final table
            n_entries = 15  # Må bare være minst like stor
            n_cols = 9
            coeff_matrix = np.zeros([n_entries, n_cols])
            rsquared_array = np.zeros(n_cols)
            aic_array = np.zeros(n_cols)
            n_obs_array = np.zeros(n_cols)
            p_values_matrix = np.zeros([n_entries, n_cols])
            std_errs_matrix = np.zeros([n_entries, n_cols])

            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_benchmark, prints=0)

            m_col = 0
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # ILLIQ - Return
            x = returns_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)

            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # ILLIQ  - Return with 1 lag
            x = returns_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # ILLIQ - Volume
            x = log_volumes_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # ILLIQ - Volume with lag
            x = log_volumes_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # ILLIQ  - Volatility
            x = log_rvol_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # ILLIQ - Volatility with lag
            x = log_rvol_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Contemporaneous
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_contemporary, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Lagged variables
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_lagged, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            first_col_entries = ['Intercept', '$illiq^D$', '$illiq^W$', '$illiq^{2M}$', '$r_t$', '$r_{t-1}$', '$v_{t}$',
                                 '$v_{t-1}$', '$rv_{t}$', '$rv_{t-1}$', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']

            first_col = []
            j = 0
            for data_r in range(0, len(first_col_entries)):
                first_col.append(first_col_entries[data_r])
                for k in range(len(first_col_entries[data_r]),
                               18):  # Tallet her skal være lengden på den lengste entrien
                    first_col[j] += ' '  # Passer på at alle blir like lange
                j += 1
                if data_r < 10:
                    first_col.append('                  ')  # De første 10 radene skal ha mellomrom mellom seg
                    j += 1

            print_rows = []
            # Fyller starten med tomromm så det blir lettere å se
            for data_r in range(0, n_rows):
                print_rows.append('        ')
            for print_r in range(0, n_rows):
                print_rows[print_r] += (first_col[print_r]) + "&"

            # Dette er benchmarken
            data_r = 0
            for print_r in range(0, 8, 2):
                for c in range(0, n_cols):
                    print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                    p_values_matrix[data_r, c], type="coeff")
                    print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                                        type="std_err")
                data_r += 1

            # Dette er regresjonene mot en og en annen variabel
            for print_r in range(8, 20, 2):
                data_r = 11
                for c in range(0, n_cols):
                    if c == int(print_r / 2) - 3:
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                        p_values_matrix[data_r, c], type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                                            type="std_err")
                        data_r += 1
                    elif c == 7 and (print_r == 8 or print_r == 12 or print_r == 16):
                        i_cont = 11 + int((print_r - 8) / 4)
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[i_cont, c],
                                                        p_values_matrix[i_cont, c], type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[i_cont, c],
                                                            type="std_err")
                    elif c == 8 and (print_r == 10 or print_r == 14 or print_r == 18):
                        i_lag = 11 + int((print_r - 10) / 4)
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[i_cont, c],
                                                        p_values_matrix[i_cont, c], type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[i_lag, c],
                                                            type="std_err")
                    else:
                        print_rows[print_r] += "           &"
                        print_rows[print_r + 1] += "           &"

            # Dette fikser de tre nedreste radene
            print_rows = supp.final_three_rows(print_rows, n_obs_array, rsquared_array, aic_array, n_cols, n_rows)

            print()
            print()
            print(
                "           -----------------------------------------Regression table for ILLIQ----------------------------------------")
            print()
            print()
            supp.final_print_regressions_latex(print_rows)  # Gjør hele printejobben

        if return_multi == 1:

            Y = returns_days[max_lag: len(returns_days)]
            n_entries = len(Y)
            start_index = len(returns_days) - n_entries
            end_index = len(returns_days)
            X = []

            # print("Return")
            # print("----------------------------------------------------------------------------------------------------------------------------")
            # print("----------------------------------------------------------------------------------------------------------------------------")

            for j in range(n_lags):
                # print("x%i: Returns with %i days lag" % (j + 1, lags[j]))
                x = supp.mean_for_n_entries(returns_days, lags[j])
                x = np.matrix(x[len(x) - n_entries: len(x)])
                if j == 0:
                    X = x
                else:
                    X = np.append(X, x, axis=0)

            X_benchmark = np.transpose(X)  # Har model

            X_benchmark = np.append(X_benchmark, mon, axis=1)
            X_benchmark = np.append(X_benchmark, tue, axis=1)
            X_benchmark = np.append(X_benchmark, wed, axis=1)
            X_benchmark = np.append(X_benchmark, thu, axis=1)
            X_benchmark = np.append(X_benchmark, fri, axis=1)
            X_benchmark = np.append(X_benchmark, sat, axis=1)
            X_benchmark = np.append(X_benchmark, sun, axis=1)

            X_contemporary = X_benchmark
            X_lagged = X_benchmark

            # These tables are 27 rows tall, 11 wide
            n_rows = 27  # in final table
            n_entries = 18  # Må bare være minst like stor
            n_cols = 11
            coeff_matrix = np.zeros([n_entries, n_cols])
            rsquared_array = np.zeros(n_cols)
            aic_array = np.zeros(n_cols)
            n_obs_array = np.zeros(n_cols)
            p_values_matrix = np.zeros([n_entries, n_cols])
            std_errs_matrix = np.zeros([n_entries, n_cols])

            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_benchmark, prints=0)

            m_col = 0
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Return - Volume
            x = log_volumes_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Return - Volume with lag
            x = log_volumes_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Return - Volatility
            x = log_rvol_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Return - Volatility with lag
            x = log_rvol_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Return - Spread
            x = spread_days[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Return - Spread with lag
            x = spread_days[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Return - ILLIQ
            x = illiq[start_index: end_index]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_contemporary = np.append(X_contemporary, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Return - ILLIQ with lag
            x = illiq[start_index - 1: end_index - 1]
            x = np.transpose(np.matrix(x))
            X = np.append(X_benchmark, x, axis=1)
            X_lagged = np.append(X_lagged, x, axis=1)
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            # Contemporaneous
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_contemporary, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            #  Lagged
            coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X_lagged, prints=0)

            m_col += 1
            coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
                import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                                   std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)

            first_col_entries = ['Intercept', '$r^D$', '$r^W$', '$r^{2M}$', '$v_t$', '$v_{t-1}$', '$rv_{t}$',
                                 '$rv_{t-1}$', '$bas_{t}$', '$bas_{t-1}$', '$illiq_{t}$', '$illiq_{t-1}$',
                                 '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']

            first_col = []
            j = 0
            for data_r in range(0, len(first_col_entries)):
                first_col.append(first_col_entries[data_r])
                for k in range(len(first_col_entries[data_r]),
                               18):  # Tallet her skal være lengden på den lengste entrien
                    first_col[j] += ' '  # Passer på at alle blir like lange
                j += 1
                if data_r < 12:
                    first_col.append('                  ')  # De første 10 radene skal ha mellomrom mellom seg
                    j += 1

            print_rows = []
            # Fyller starten med tomromm så det blir lettere å se
            for data_r in range(0, n_rows):
                print_rows.append('        ')
            for print_r in range(0, n_rows):
                print_rows[print_r] += (first_col[print_r]) + "&"

            # Dette er benchmarken
            data_r = 0
            for print_r in range(0, 8, 2):
                for c in range(0, n_cols):
                    print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                    p_values_matrix[data_r, c], type="coeff")
                    print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                                        type="std_err")
                data_r += 1

            # Dette er regresjonene mot en og en annen variabel
            for print_r in range(8, 24, 2):
                data_r = 11
                for c in range(0, n_cols):
                    if c == int(print_r / 2) - 3:
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[data_r, c],
                                                        p_values_matrix[data_r, c], type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[data_r, c],
                                                            type="std_err")
                        data_r += 1
                    elif c == 9 and (print_r == 8 or print_r == 12 or print_r == 16 or print_r == 20):
                        i_cont = 11 + int((print_r - 8) / 4)
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[i_cont, c],
                                                        p_values_matrix[i_cont, c], type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[i_cont, c],
                                                            type="std_err")
                    elif c == 10 and (print_r == 10 or print_r == 14 or print_r == 18 or print_r == 22):
                        i_lag = 11 + int((print_r - 10) / 4)
                        print_rows[print_r] = fmt_print(print_rows[print_r], coeff_matrix[i_lag, c],
                                                        p_values_matrix[i_lag, c], type="coeff")
                        print_rows[print_r + 1] = fmt_print(print_rows[print_r + 1], std_errs_matrix[i_lag, c],
                                                            type="std_err")
                    else:
                        print_rows[print_r] += "           &"
                        print_rows[print_r + 1] += "           &"

            print_rows = supp.final_three_rows(print_rows, n_obs_array, rsquared_array, aic_array, n_cols, n_rows)

            print()
            print()
            print(
                "           -----------------------------------------Regression table for Return----------------------------------------")
            print()
            print()
            supp.final_print_regressions_latex(print_rows)  # Gjør hele printejobben

    if autoreg == 1:  # Er ikke oppdatert med ny output!
        print_n(20)
        print("Rolls regression:")
        linreg.autocorr_linreg(spread_days, 1, max_lag=60)
        print_n(5)
        # print("Log-ILLIQ regression:")
        # linreg.autocorr_linreg(log_illiq_days, 22)
