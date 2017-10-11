import data_import as di
import plot
import sondre_support_formulas as supp
import jacob_support as jake_supp

exchanges, time_list, prices, volumes, total_price, total_volume, currency = di.get_lists(2, 1)
print(total_price[0:100])
returns = jake_supp.logreturn(total_price[0:100])
volume = total_volume[0:100]
plot.scatters(volume, returns)
