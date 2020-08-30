# Alan's Stock Trader Bot
# 08/29/2020
# Written in Python 3
#
# Run this script daily as a scheduled task or cronjob.
# NOTE: The majority of this script was written in a single night, so DO NOT trust this algoritm with large amounts of money. Further testing is needed.
#
# This script will monitor a given set of stock tickers and make educated predictions on when to trigger buys and sells based on the exponential moving average crossover strategy.
#
# Documentation Links:
#	https://github.com/RomelTorres/alpha_vantage
# 	https://www.alphavantage.co/documentation/
#	https://robin-stocks.readthedocs.io/en/latest/quickstart.html
#	https://robin-stocks.readthedocs.io/en/latest/functions.html

#import statements
import os
import time
from datetime import date
import robin_stocks
from dotenv import load_dotenv
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
from yahoo_fin import stock_info as si
import csv

#log start of daily run
with open('transaction-log.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["DAILY RUN", str(date.today()), "STARTED"])

#load and set env variables
load_dotenv()
ROBINHOOD_USERNAME = os.getenv("ROBINHOOD_USERNAME")
ROBINHOOD_PASSWORD = os.getenv("ROBINHOOD_PASSWORD")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

#set variables
monitored_tickers = ['XLTD', 'VIVO', 'ODT', 'CODX', 'APPS']
current_price = 0.0
share_qty = 1

pd.set_option("display.max_rows", None, "display.max_columns", None)

#Alpha Vantage connection info
ts = TimeSeries(key='ALPHA_VANTAGE_API_KEY', output_format='pandas')
ti = TechIndicators(key='ALPHA_VANTAGE_API_KEY', output_format='pandas')

for ticker in monitored_tickers:
	#set variables
	day_emas = []
	week_emas = []
	keys = []
	vals = []
	intersections = []
	sell_triggers = []
	buy_triggers = []

	#get current stock price
	current_price = si.get_live_price(ticker)
	print("_____________________ " + ticker + " - [" + str(current_price) + "]")

	#get actual price
	actual_data, meta_data = ts.get_weekly(symbol=ticker)

	#get day ema
	day_ema, meta_deta = ti.get_ema(symbol=ticker,interval='daily')

	#get weekly ema
	weekly_ema, meta_deta = ti.get_ema(symbol=ticker,interval='weekly')

	for val in day_ema.iterrows():
		day_emas.append([val[0],val[1].values])
	for val in weekly_ema.iterrows():
		week_emas.append([val[0],val[1].values])

	for day in day_emas:
		for week in week_emas:
			if week[0] == day[0]:
				#print(week[1][0])
				#print(day[1][0])
				#print("Date: " + str(day[0]) + " : day ema Price: " + str(day[1][0]) + " : week ema Price: " + str(week[1][0]))
				keys.append([day[0], day[1][0], week[1][0], ticker])
				vals.append(day[1][0] - week[1][0])

	for i, v in enumerate(vals):
		if i > 0:
			if v / vals[i-1] < 0:
				intersections.append(keys[i])
				#print("Intersection Happened: " + str(keys[i]))

	#decide if the intersection triggers a buy or sell
	#if the week ema is less than the month ema, sell; if the week ema is more than the month ema, buy
	for intersect in intersections:
		if intersect[1] < intersect[2]:
			sell_triggers.append(intersect)
		elif intersect[1] > intersect[2]:
			buy_triggers.append(intersect)

	print("____________________ v BUY TRIGGERS  v ____________________")
	for buy in buy_triggers:
		print("Buy Trigger: " + str(buy))
	print("____________________ ^ BUY TRIGGERS  ^ ____________________")
	print("____________________ v SELL TRIGGERS v ____________________")
	for sell in sell_triggers:
		print("Sell Trigger: " + str(sell))
	print("____________________ ^ SELL TRIGGERS ^ ____________________")

	#if the latest buy trigger is today's date, place Robinhood order
	if str(date.today()) == str(sell_triggers[-1][0].to_pydatetime())[:10]:
		print("##### STOCK BUY HAS BEEN TRIGGERED #####")
		with open('transaction-log.csv', 'w', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(["BUY", ticker, str(date.today()), str(current_price), "STARTED"])

		#log into Robinhood using credentials in the .env file
		print("Logging you into: " + ROBINHOOD_USERNAME)
		login = robin_stocks.authentication.login(username=ROBINHOOD_USERNAME, password=ROBINHOOD_PASSWORD, store_session=False)

		#plot data with matplotlib, this will hold up code execution until the graph window is exited
		ax = plt.gca()
		actual_data['4. close'].plot(ax=ax,label='Actual Price')
		day_ema.plot(ax=ax,label='day ema')
		weekly_ema.plot(ax=ax,label='weekly ema')
		plt.legend(loc='best')
		plt.title(ticker)
		plt.grid()
		plt.show()

		#prompt user to continue with buy
		answer = None
		while answer not in ("y", "n"): 
			answer = input("Proceed with buy? (y/n) ") 
			if answer == "y": 
				#buy qty of specified stock from Robinhood
				#robin_stocks.order_buy_market(ticker, share_qty) #uncomment this when you want the script to actually place the buy in Robinhood
				print("Bought " + str(share_qty) + " share(s) of " + ticker + " on " + str(date.today()) + " at $" + str(current_price))
				with open('transaction-log.csv', 'w', newline='') as file:
				    writer = csv.writer(file)
				    writer.writerow(["BUY", ticker, str(date.today()), str(current_price), "COMPLETE"])
			elif answer == "n": 
				with open('transaction-log.csv', 'w', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(["BUY", ticker, str(date.today()), str(current_price), "MANUALLY CANCELLED"])
			else: 
		 		print("Please enter y or n")

	#if the latest sell trigger is today's date, sell shares of that stock
	elif str(date.today()) == str(sell_triggers[-1][0].to_pydatetime())[:10]:
		print("##### STOCK SELL HAS BEEN TRIGGERED #####")
		with open('transaction-log.csv', 'w', newline='') as file:
				    writer = csv.writer(file)
				    writer.writerow(["SELL", ticker, str(date.today()), str(current_price), "STARTED"])

		#log into Robinhood using credentials in the .env file
		print("Logging you into: " + ROBINHOOD_USERNAME)
		login = robin_stocks.authentication.login(username=ROBINHOOD_USERNAME, password=ROBINHOOD_PASSWORD, store_session=False)

		#plot data with matplotlib, this will hold up code execution until the graph window is exited
		ax = plt.gca()
		actual_data['4. close'].plot(ax=ax,label='Actual Price')
		day_ema.plot(ax=ax,label='day ema')
		weekly_ema.plot(ax=ax,label='weekly ema')
		plt.legend(loc='best')
		plt.title(ticker)
		plt.grid()
		plt.show()

		#prompt user to continue with sell
		answer = None
		while answer not in ("y", "n"): 
			answer = input("Proceed with sell? (y/n) ") 
			if answer == "y": 
				#sell qty of specified stock from Robinhood
				#robin_stocks.order_sell_market(ticker, share_qty) #uncomment this when you want the script to actually place the sell in Robinhood
				print("Sold " + str(share_qty) + " share(s) of " + ticker + " on " + str(date.today()) + " at $" + str(current_price))
				with open('transaction-log.csv', 'w', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(["SELL", ticker, str(date.today()), str(current_price), "COMPLETE"])
			elif answer == "n": 
				with open('transaction-log.csv', 'w', newline='') as file:
					writer = csv.writer(file)
					writer.writerow(["SELL", ticker, str(date.today()), str(current_price), "MANUALLY CANCELLED"])
			else: 
		 		print("Please enter y or n")

	time.sleep(60) #sleep for a minute to wait out the query limit on the free AlphaVantage API

#log completion of daily run
with open('transaction-log.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["DAILY RUN", str(date.today()), "COMPLETE"])

robin_stocks.authentication.logout()