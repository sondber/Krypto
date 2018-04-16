import numpy as np
import data_import as di
import regression_support
from Sondre import sondre_support_formulas as supp
import data_import_support as dis
import plot


exchanges = ["korbit"]
hours_in_window = [1, 2, 4]      # La denne være en liste med de forskjellige vinduene analysen skal gjøres for
convert_coeffs_to_percentage = 1    # Convert coeffs and std.errs. of returnsH and spreadH to percentage
convert_logs = 0                    # Convert coeffs and std.errs. of rvol and illiq to percentage, i.e. 100*exp(coeff) NB! Doesn't work
subtract_means = 1
log_illiqs = True


for exc in exchanges:
    exc_name, time_listH, returnsH, spreadH, volumesH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = di.get_list(
        exc=exc, freq=1, local_time=1)

    hour = supp.fix_time_list(time_listH)[3]

    print()
    print("------------------------ INTRADAY REGRESSION FOR", exc_name.upper()[0:-3], "-------------------------")
    print()


    print()
    print("     ------------------------------------------------Regression table for Intraday seasonality-----------------------------------------")


    n = len(hour)
    for h in hours_in_window:   # Itererer over de forskjellige vinduene
        single_hour, two_hours, three_hours, four_hours = [0, 0, 0, 0]  # initialize

        # Sjekker nå hvor mange timer det er i vinduet i denne interasjonen
        if h == 1:
            single_hour = 1
        elif h == 2:
            two_hours = 1
        elif h == 3:
            three_hours = 1
        else:
            four_hours = 1

        if single_hour == 1:
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


            X = np.matrix(zero)
            X = np.append(X, np.matrix(one), axis=0)
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

            n_entries = 24  # Må bare være minst like stor som antall forklaringsvariable
            n_rows = 3 + n_entries * 2  # in final table

        elif two_hours == 1:
            first = np.zeros(n)
            second = np.zeros(n)
            third = np.zeros(n)
            fourth = np.zeros(n)
            fifth = np.zeros(n)
            sixth = np.zeros(n)
            seventh = np.zeros(n)
            eigth = np.zeros(n)
            nineth = np.zeros(n)
            tenth = np.zeros(n)
            eleventh = np.zeros(n)
            twelwth = np.zeros(n)

            first_period = [0, 1]
            second_period = [2, 3]
            third_period = [4, 5]
            fourth_period = [6, 7]
            fifth_period = [8, 9]
            sixth_period = [10, 11]
            seventh_period = [12, 13]
            eighth_period = [14, 15]
            nineth_period = [16, 17]
            tenth_period = [18, 19]
            eleventh_period = [20, 21]
            twelwth_period = [22, 23]

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
                elif hr in fifth_period:
                    fifth[i] = 1
                elif hr in sixth_period:
                    sixth[i] = 1
                elif hr in seventh_period:
                    seventh[i] = 1
                elif hr in eighth_period:
                    eigth[i] = 1
                elif hr in nineth_period:
                    nineth[i] = 1
                elif hr in tenth_period:
                    tenth[i] = 1
                elif hr in eleventh_period:
                    eleventh[i] = 1
                elif hr in twelwth_period:
                    twelwth[i] = 1

            X = np.matrix(first)
            X = np.append(X, np.matrix(second), axis=0)
            X = np.append(X, np.matrix(third), axis=0)
            X = np.append(X, np.matrix(fourth), axis=0)
            X = np.append(X, np.matrix(fifth), axis=0)
            X = np.append(X, np.matrix(sixth), axis=0)
            X = np.append(X, np.matrix(seventh), axis=0)
            X = np.append(X, np.matrix(eigth), axis=0)
            X = np.append(X, np.matrix(nineth), axis=0)
            X = np.append(X, np.matrix(tenth), axis=0)
            X = np.append(X, np.matrix(eleventh), axis=0)
            X = np.append(X, np.matrix(twelwth), axis=0)
            X = np.transpose(X)

            n_entries = 12  # Antall forklaringsvariable
            n_rows = 3 + n_entries * 2  # in final table

        elif three_hours == 1:
            first = np.zeros(n)
            second = np.zeros(n)
            third = np.zeros(n)
            fourth = np.zeros(n)
            fifth = np.zeros(n)
            sixth = np.zeros(n)
            seventh = np.zeros(n)
            eigth = np.zeros(n)

            first_period = [0, 1, 2]
            second_period = [3, 4, 5]
            third_period = [6, 7, 8]
            fourth_period = [9, 10, 11]
            fifth_period = [12, 13, 14]
            sixth_period = [15, 16, 17]
            seventh_period = [18, 19, 20]
            eighth_period = [21, 22, 23]

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
                elif hr in fifth_period:
                    fifth[i] = 1
                elif hr in sixth_period:
                    sixth[i] = 1
                elif hr in seventh_period:
                    seventh[i] = 1
                elif hr in eighth_period:
                    eigth[i] = 1

            X = np.matrix(first)
            X = np.append(X, np.matrix(second), axis=0)
            X = np.append(X, np.matrix(third), axis=0)
            X = np.append(X, np.matrix(fourth), axis=0)
            X = np.append(X, np.matrix(fifth), axis=0)
            X = np.append(X, np.matrix(sixth), axis=0)
            X = np.append(X, np.matrix(seventh), axis=0)
            X = np.append(X, np.matrix(eigth), axis=0)
            X = np.transpose(X)

            n_entries = 8  # Må bare være minst like stor som antall forklaringsvariable
            n_rows = 3 + n_entries * 2  # in final table

        elif four_hours == 1:
            first = np.zeros(n)
            second = np.zeros(n)
            third = np.zeros(n)
            fourth = np.zeros(n)
            fifth = np.zeros(n)
            sixth = np.zeros(n)

            first_period = [0, 1, 2, 3]
            second_period = [4, 5, 6, 7]
            third_period = [8, 9, 10, 11]
            fourth_period = [12, 13, 14, 15]
            fifth_period = [16, 17, 18, 19]
            sixth_period = [20, 21, 22, 23]

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
                elif hr in fifth_period:
                    fifth[i] = 1
                elif hr in sixth_period:
                    sixth[i] = 1

            X = np.matrix(first)
            X = np.append(X, np.matrix(second), axis=0)
            X = np.append(X, np.matrix(third), axis=0)
            X = np.append(X, np.matrix(fourth), axis=0)
            X = np.append(X, np.matrix(fifth), axis=0)
            X = np.append(X, np.matrix(sixth), axis=0)
            X = np.transpose(X)

            n_entries = 6  # antall forklaringsvariable
            n_rows = 3 + n_entries * 2  # in final table

        n_cols = 5
        coeff_matrix = np.zeros([n_entries, n_cols])
        rsquared_array = np.zeros(n_cols)
        aic_array = np.zeros(n_cols)
        n_obs_array = np.zeros(n_cols)
        p_values_matrix = np.zeros([n_entries, n_cols])
        std_errs_matrix = np.zeros([n_entries, n_cols])

        m_col = 0

        Y = returnsH
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=0)
        Y = log_volumesH
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=0)
        Y = log_rvolH
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=0)
        Y = spreadH
        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array, intercept=0, prints=0)

        if log_illiqs == True:
            Y = log_illiqH # LOG / LINEAR !
        else:
            Y = illiqH  # LOG / LINEAR !


        m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
            m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
            intercept=0, prints=0)

        if subtract_means == 1:  # Turns analysis into
            # Now we need to subtract the means from the coefficient matrix
            returnsH -= np.mean(coeff_matrix[:, 0])
            log_volumesH -= np.mean(coeff_matrix[:, 1])
            log_rvolH -= np.mean(coeff_matrix[:, 2])
            spreadH -= np.mean(coeff_matrix[:, 3])

            if log_illiqs == True:
                log_illiqH -= np.mean(coeff_matrix[:, 4])
            else:
                illiqH -= np.mean(coeff_matrix[:, 4])

            m_col = 0
            coeff_matrix = np.zeros([n_entries, n_cols])
            rsquared_array = np.zeros(n_cols)
            aic_array = np.zeros(n_cols)
            n_obs_array = np.zeros(n_cols)
            p_values_matrix = np.zeros([n_entries, n_cols])
            std_errs_matrix = np.zeros([n_entries, n_cols])

            Y = returnsH
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0)
            Y = log_volumesH
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0)
            Y = log_rvolH
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0)
            Y = spreadH
            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0, prints=0)

            if log_illiqs == True:
                Y = log_illiqH  # LOG / LINEAR !
            else:
                Y = illiqH  # LOG / LINEAR !

            m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = regression_support.import_regressions(
                m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array,
                intercept=0, prints=0)

        if convert_coeffs_to_percentage == 1:
            print()
            print()
            print()
            print("NB!! Converting returnsH and spreadH back into percentage")
            c = 0  # returnsH
            for i in range(0, n_entries):
                coeff_matrix[i, c] = 100 * coeff_matrix[i, c]
                std_errs_matrix[i, c] = 100 * std_errs_matrix[i, c]
            c = 3  # spreadH
            for i in range(0, n_entries):
                coeff_matrix[i, c] = 100 * coeff_matrix[i, c]
                std_errs_matrix[i, c] = 100 * std_errs_matrix[i, c]

            if convert_logs == 1:  # This logic is not sound. e^(error) does not make sense
                print("NB!! Converting rvol and illiq back into percentage")
                c = 2  # rvol
                for i in range(0, n_entries):
                    coeff_matrix[i, c] = 100 * np.exp(coeff_matrix[i, c])
                    std_errs_matrix[i, c] = 100 * np.exp(std_errs_matrix[i, c])
                c = 4  # illiq
                for i in range(0, n_entries):
                    coeff_matrix[i, c] = 100 * np.exp(coeff_matrix[i, c])
                    std_errs_matrix[i, c] = 100 * np.exp(std_errs_matrix[i, c])

        if single_hour == 1:
            first_col_entries = ['00-01', '01-02', '02-03', '03-04', '04-05', '05-06', '06-07', '07-08', '08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16',
                                 '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-00', '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']
        elif two_hours == 1:
            first_col_entries = ['00:00-01:59', '02:00-03:59', '04:00-05:59', '06:00-07:59', '08:00-09:59', '10:00-11:59',
                                 '12:00-13:59', '14:00-15:59', '16:00-17:59', '18:00-19:59', '20:00-21:59', '22:00-23:59',
                                 '\\textit{\\# Obs.}', '$R^2$', '\\textit{AIC}']
        elif three_hours == 1:
            first_col_entries = ['00:00-02:59', '03:00-05:59', '06:00-08:59', '09:00-11:59', '12:00-14:59', '15:00-17:59',
                                 '18:00-20:59', '21:00-23:59', '\\textit{\\# Obs.}', '$R^2$',
                                 '\\textit{AIC}']
        elif four_hours == 1:
            first_col_entries = ['00:00-03:59', '04:00-07:59', '08:00-11:59', '12:00-15:59', '16:00-19:59', '20:00-23:59',
                                 '\\textit{\\# Obs.}', '$R^2$',
                                 '\\textit{AIC}']
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

        print()

        print_rows = []
        # Fyller starten med tomromm så det blir lettere å se
        for i in range(0, n_rows):
            print_rows.append('        ')
        for r in range(0, n_rows):
            print_rows[r] += (first_col[r]) + "&"

        i = 0
        for r in range(0, n_rows - 3, 2):
            for c in range(0, n_cols):
                print_rows[r] = regression_support.fmt_print(print_rows[r], coeff_matrix[i, c], p_values_matrix[i, c], type="coeff")
                print_rows[r + 1] = regression_support.fmt_print(print_rows[r + 1], std_errs_matrix[i, c], type="std_err")
            i += 1


        # Dette fikser de tre nedreste radene
        print_rows = regression_support.final_three_rows(print_rows, n_obs_array, rsquared_array, aic_array, n_cols, n_rows)


        print()
        print("     ------------------------------------------------", str(exc_name),
              "-----------------------------------------")

        regression_support.final_print_regressions_latex(print_rows)  # Gjør hele printejobben
