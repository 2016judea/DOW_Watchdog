"""
Author: Aidan Jude
Date: 07/01/2018
Description:
    This program is responsible for checking the current stock market price against the 52 week low (for the same stock)
    and if the current stock price is lower then the 52 week low, we know it is a good opportunity to purchase stock. Hence,
    a text message is sent to notify the designated recipient.

Worthwhile notes:
    This program also checks if the current 52 week low is lower then that of the previous 52 week low (stored in a text file).
    This serves as a fail safe since a stock could have dropped below a 52 week low, and since came back up in value. If this
    is the case, then the current stock price is not a true tell of whether the stock is a viable option for purchase. This check
    allows for a program to be scheduled to run at times that are farther apart, an hour perhaps, since there is less of a need
    for continuous stock price checks. This also allows a reduction is Yahoo Finance server requests and lowers the chances of
    having one's IP address blacklisted.
"""

from Stock_Price_Fetch import *
from SP_500 import *
import smtplib
from email.mime.text import MIMEText

#utilize a gmail account to send the desired text messages
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login('YOUR_EMAIL', 'EMAIL_PASSWORD')
#designate a text file to hold the former 52 week lows for each stock we are monitoring
text_file = 'Stock_Daily_Lows.txt'
count = 0
counter = 0
year_low_flag = False

while count < len(sp_500_symbols):
    if get_curr_price(sp_500_symbols[count]) != -1 and get_52_wk_low(sp_500_symbols[count]) != -1:
        FILE = open(text_file, 'r')
        content = FILE.read()
        FILE.close()
        #if a stock's 52 week low has not been logged to the text file, do so
        if str(sp_500_symbols[count]) not in content:
            FILE_App = open(text_file, 'a')
            FILE_App.write(str(sp_500_symbols[count]) + ":" + str(get_52_wk_low(sp_500_symbols[count])) + "\n")
            FILE_App.close()
        #otherwise, we need to compare the former 52 week low to the current and determine if a notification needs to be sent
        else:
            index = content.find(str(sp_500_symbols[count]))
            loop_start = index + len(str(sp_500_symbols[count]) + ':')
            original = loop_start
            low = ''
            while content[loop_start].isnumeric() or content[loop_start] == '.':
                low += content[loop_start]
                loop_start += 1
                counter += 1
                if counter > 15:
                    break
            counter = 0
            if float(get_52_wk_low(sp_500_symbols[count])) < float(low):
                FILE_App = open(text_file, 'w').close()
                to_write = str(get_52_wk_low(sp_500_symbols[count]))
                beginning = content[:(original)]
                ending = content[original + len(low):]
                content = beginning + to_write + ending
                FILE_App = open(text_file, 'w')
                FILE_App.write(content)
                FILE_App.close()
                year_low_flag = True
    #if the current stock price is <= the 52 week low and/or current 52 week low was recently established, send a text message notification
    if float(get_curr_price(sp_500_symbols[count])) <= float(get_52_wk_low(sp_500_symbols[count])) or year_low_flag == True:
        message = MIMEText(str(sp_500_symbols[count]) + " has hit a 52 week low of: $" + str(get_curr_price(sp_500_symbols[count])))
        message['Subject'] = '...Stock Price Alert...'
        server.sendmail('DOW_Watchdog', 'PHONE_NUMBER', message.as_string())
        year_low_flag = False
    count += 1
