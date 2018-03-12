import numpy as np
import data_import as di
import data_import_support as dis
from Sondre import sondre_support_formulas as supp

# 1 kontrollpanel
log_illiqs = 1 # Should log-illiq be used rather than plain illiq?
hours_in_period = 4
spread_determinants = 1

# 2 importere prices, volumes
exchange_list, time_listM, pricesM, volumesM = di.get_lists(opening_hours="n", make_totals="n")
exchanges = [1]  # just for testing

# 3 iterere over exchanges
for exc in exchanges:
    # 4 importere clean_trans_hours
    time_listH, returnsH, spreadH, log_volumesH, illiqH, log_illiqH, rvolH, log_rvolH = dis.clean_trans_hours(time_listM, pricesM, volumesM, exc=exc)

    if log_illiqs:
        illiqH = log_illiqH

    # 5 standardisere
    stdzd_log_volumes = supp.standardize(log_volumesH)
    stdzd_spread = supp.standardize(spreadH)
    stdzd_illiq = supp.standardize(illiqH)
    stdzd_returns = supp.standardize(returnsH)
    stdzd_log_rvol = supp.standardize(log_rvolH)

    if spread_determinants == 1:

        Y = stdzd_spread
        n_cols = 9  # 10 for BAS og for ILLIQ

        # 6 lage benchmark
        Y, X_benchmark, n_entries, max_lag = supp.benchmark_hourly(Y, time_listH, HAR_config=0, hours_in_period=hours_in_period)

        # 7 Initialisere final table (linje 70 i intraweek)
        coeff_matrix = np.zeros([n_entries, n_cols])
        rsquared_array = np.zeros(n_cols)
        aic_array = np.zeros(n_cols)
        n_obs_array = np.zeros(n_cols)
        p_values_matrix = np.zeros([n_entries, n_cols])
        std_errs_matrix = np.zeros([n_entries, n_cols])


        X_contemporary = X_benchmark
        X_lagged = X_benchmark

        # 8 Kjøre regresjonen for alle Y

        # 9 trekke fra mean
        # 9.1 Kjøre regressjonene på nytt med mean trukket fra
        # 10 Convert coeffs to percentage
        # 11 Lage prints
        # 12 printe til latex


