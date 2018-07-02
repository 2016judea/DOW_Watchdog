"""
Author: Aidan Jude
Date: 07/01/2018
Description:
    This file is used to define the functions utilized in the DOW_Watchdog
    program file. These functions utilize the urllib.request library to fetch
    current stock prices as well as 52 week lows based on a given stock symbol.
"""

import urllib.request

#opens the url for the given stock and translates the unicode HTML into a string
def get_curr_price(symbol):
    base_url = 'http://finance.yahoo.com/quote/'
    content = urllib.request.urlopen(base_url + symbol).read()
    cont_str = content.decode("utf8")
    index = cont_str.find('"regularMarketPrice":{"raw":')
    #set the starting location for the stock price
    loop_start = index + len('"regularMarketPrice":{"raw":') - 1
    count = 0
    price = ''

    while cont_str[loop_start + 1].isnumeric() or cont_str[loop_start + 1] == '.':
        price += cont_str[loop_start + 1]
        loop_start += 1
        count += 1
        if count > 15:
            break
    #return price as -1 if the price could not be obtained
    if count > 15:
        price = -1
    
    return price

def get_52_wk_low(symbol):
    base_url = 'http://finance.yahoo.com/quote/'
    content = urllib.request.urlopen(base_url + symbol).read()
    cont_str = content.decode("utf8")
    index = cont_str.find('"fiftyTwoWeekRange":{"raw":')
    loop_start = index + len('"fiftyTwoWeekRange":{"raw":')
    count = 0
    price = ''
    
    while cont_str[loop_start + 1].isnumeric() or cont_str[loop_start + 1] == '.':
        price += cont_str[loop_start + 1]
        loop_start += 1
        count += 1
        if count > 15:
            break
    if count > 15:
        price = -1

    return price
