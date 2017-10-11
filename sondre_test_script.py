import data_import as di
import plot
import sondre_support_formulas as supp
import jacob_support as jake_supp

exchanges, time_list, prices, volumes, total_price, total_volume, currency = di.get_lists(1, 1)
returns = jake_supp.logreturn(total_price)
time_list_rolls, rolls = supp.get_rolls()

print(rolls)
print(len(rolls))
print(len(returns))

axes = plot.plt.gca()

plot.plt.figure(1)
axes.set_xlim([0, 10000])
axes.set_ylim([-0.05, 0.05])
plot.scatters(total_volume, returns)

plot.plt.figure(2)
plot.scatters(total_volume, rolls)
plot.plt.show()
