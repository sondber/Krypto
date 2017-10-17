import numpy as np
import data_import as di
import plot
from Jacob import jacob_support as jake_supp
from Sondre import sondre_support_formulas as supp

exchanges, time_list, prices, volumes, total_price, total_volume, currency = di.get_lists("h")
returns = jake_supp.logreturn(total_price)
time_list_rolls, rolls = supp.get_rolls()
year, month, day, hour, minute = supp.fix_time_list(time_list)

plot.plt.figure(1)
axes = plot.plt.gca()
axes.set_xlim([0, 1000])
axes.set_ylim([-0.05, 0.05])
plot.scatters(total_volume, returns)
plot.plt.title("Returns vs. volume")
ccf = np.corrcoef(total_volume, returns)[0,1]
print("Correlation coefficient = %0.2f" % ccf)


plot.plt.figure(2)
axes = plot.plt.gca()
axes.set_xlim([0, 1000])
axes.set_ylim([0, 0.002])
plot.scatters(total_volume, rolls)
plot.plt.title("Liquidity vs. volume")
ccf = np.corrcoef(total_volume, rolls)[0,1]
print("Correlation coefficient = %0.2f" % ccf)

# Skal være en kode som itererer gjennom årene og lager scatters på liquidity
plot.plt.figure(4)
axes = plot.plt.gca()
axes.set_xlim([0, 1000])
axes.set_ylim([0, 0.002])
i = 0
for yr in range(2013, 2018):
    temp_y = []
    temp_x = []
    yearcheck = 1
    while yearcheck:
        try:
            temp_y.append(rolls[i])
            temp_x.append(total_volume[i])
        except IndexError:
            print("error")
        i = i + 1
        try:
            if year[i] == yr:
                yearcheck = 1
            else:
                yearcheck = 0
        except IndexError:
            yearcheck = 0
    print("\nYear : %i" % yr)
    ccf = np.corrcoef(temp_x, temp_y)[0,1]
    print("Correlation coefficient = %0.2f" % ccf)
    if yr == 2013:
        clr = "black"
    elif yr == 2014:
        clr = "blue"
    elif yr == 2015:
        clr = "red"
    elif yr == 2016:
        clr = "green"
    elif yr == 2017:
        clr = "purple"
    plot.scatters(temp_x, temp_y, color=clr, label=str(yr))

plot.plt.show()

