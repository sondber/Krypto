# import support_formulas as supp


def input_trans(inp):
    if inp == "y" or inp == "Y" or inp == "yes" or inp == "Yes" or inp == '1':
        res = 1
    elif inp == "n" or inp == "N" or inp == "no" or inp == "No" or inp == '0':
        res = 0
    else:
        res = 0
    return res


def import_data():
    inp = input("Default settings? \
(Bistamp, No currency conversion or removal of extremes) ") or 1
    defset = input_trans(inp)

    if defset == 1:
        compex = 0
        currency = 0
        no_extreme = 0
    else:

        inp = input("[0] Look at long data for Bitstamp (default) \n[1] Compare all exchanges \n")
        compex = input_trans(inp)

        if compex:
            inp = input("Convert all currencies to USD? ")
            currency = input_trans(inp)
        else:
            currency = 0

        inp = input("Should we remove extreme values? ")
        no_extreme = input_trans(inp)

    return compex, currency, no_extreme


def plots():
    inp = input("Would you like plots? ")
    any_plots = input_trans(inp)

    if any_plots:
        inp = input("Would you like volume plots? ")
        volumeplots = input_trans(inp)
        inp = input("Would you like price plots? ")
        priceplots = input_trans(inp)
        inp = input("Would you like moving average variance plots? ")
        varplots = input_trans(inp)
        inp = input("Would you like data histograms? ")
        dataplots = input_trans(inp)
    else:
        volumeplots = 0
        priceplots = 0
        varplots = 0
        dataplots = 0
    return volumeplots, priceplots, varplots, dataplots


def where_to_get_data():
    which_freq = input("Which frequency would you like? \
    \n[0] Daily \n[1] Hourly \n[2] Minute (default)\n") or 2
    which_loc = input("Where would you like the data to be collected from? \
    \n[0] Raw csv \n[1] Aggregate csv (default)\n") or 1

    which_freq = int(which_freq)
    which_loc = int(which_loc)

    return which_freq, which_loc
