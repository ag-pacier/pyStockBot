# Alan's Stock Trader Bot - Ticker Populator
# 09/01/2020
# Written in Python 3
#
# Run this script to gather a list of stock tickers from Robinhood with a specified tag and add them to the monitored-tickers.csv file to be read by trader.py

#import statements
import csv
import os
import robin_stocks
#No longer need dotenv since we will be using actual environmental variables
#from dotenv import load_dotenv

#load and set env variables
#load_dotenv()
ROBINHOOD_USERNAME = os.getenv("ROBINHOOD_USERNAME")
ROBINHOOD_PASSWORD = os.getenv("ROBINHOOD_PASSWORD")

#set variables
mt_file = "monitored-tickers.csv"
monitored_tickers = []

def append_ticker_to_csv(ticker):
	with open(mt_file, 'a', newline='') as file:
		writer = csv.writer(file)
		writer.writerow([ticker])

#log into Robinhood using credentials in the .env file
def rs_login():
	print("Logging you into: " + ROBINHOOD_USERNAME)
	login = robin_stocks.authentication.login(username=ROBINHOOD_USERNAME, password=ROBINHOOD_PASSWORD, store_session=False)

#query Robinhood for all stock tickers with a specified tag (eg. "technology") and update monitored-tickers.csv file with all stocks that have a value below ticker_max_price
def update_tickers_from_tag(tag, ticker_max_price):
	added_ticker_count = 0
	for stock in robin_stocks.get_all_stocks_from_market_tag(tag):
		if stock['symbol'] not in monitored_tickers:
			if float(stock['ask_price']) > 1.00 and float(stock['ask_price']) < ticker_max_price:
				append_ticker_to_csv(stock['symbol'])
				added_ticker_count += 1
	print("Added " + str(added_ticker_count) + " to " + mt_file)

def main():
	with open(mt_file, 'r') as ticker_file:
		csv_reader = csv.reader(ticker_file)
		for row in csv_reader:
			monitored_tickers.append(row[0])
	rs_login()
	tag = input("Enter tag to query: ")
	ticker_max_price = float(input("Enter max price: "))
	update_tickers_from_tag(tag, ticker_max_price)

if __name__ == "__main__":
    main()