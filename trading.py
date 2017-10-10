import data_import as di
import support_formulas as supp
import numpy as np

start_wallet_USD = 1000
start_wallet_BTC = 0

startdate = "201301"
enddate = "201709"

print("Loading data...")
exchanges, time_list, prices, volumes, total_price, total_volume, currency = di.get_lists(2, 1, startdate, enddate)
print("Data loaded")

price = prices[0,:]
price = price[1000000:1000020] # <------------------
returns = supp.logreturn(price)
n_mins = len(price)


wall_usd = np.zeros(n_mins)
wall_btc = np.zeros(n_mins)
buy_usd = np.zeros(n_mins)
sell_btc = np.zeros(n_mins)
buy_btc = np.zeros(n_mins)
sell_usd = np.zeros(n_mins)

wall_usd[0] = start_wallet_USD
wall_btc[0] = start_wallet_BTC
transaction_cost_perc = 0.001
transaction_cost = np.zeros(n_mins)
for i in range(1, n_mins):
    if returns[i] >= 0:
        buy_usd[i] = wall_usd[i-1]/10
    elif returns[i] < 0:
        sell_btc[i] = wall_btc[i-1]/10

    transaction_cost[i] = transaction_cost_perc * buy_usd[i]

    buy_btc[i] = buy_usd[i] * price[i]
    sell_usd[i] = sell_btc[i] / price[i]
    wall_usd[i] = wall_usd[i - 1] + sell_usd[i] - buy_usd[i] - transaction_cost[i]
    wall_btc[i] = wall_btc[i - 1] + buy_btc[i] - sell_btc[i]
    print("Initial USD in wallet: " + wall_usd[i-1])
    print("Initial BTC in wallet: " + wall_btc[i - 1])
    print("Purchase of BTC: $" + wall_btc[i - 1])


print(wall_usd[0:20])
print(buy_usd[0:20])
print(sell_usd[0:20])

final_USD = wall_usd[n_mins - 1] + wall_btc[n_mins - 1] * price[n_mins - 1]
profit = final_USD - start_wallet_USD
print("Final: \n %0.1f USD \n %0.1f BTC \nTotal value: %0.1f USD" % (wall_usd[n_mins - 1], wall_btc[n_mins - 1], final_USD))
print("Profit: $%0.1f" % profit)
print("Profit for buying 01.01.2013 and selling today: $" + str(1000*(price[n_mins-1]-price[0])))
print("Spent on transaction costs: $%0.1f " % sum(transaction_cost))