#Combined python file to be run in a container

import csv, time, sys, robin_stocks
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from yahoo_fin import stock_info as si
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import date
from datetime import datetime
from os import getenv

#Set environmental variables
ROBINHOOD_USERNAME = getenv("ROBINHOOD_USERNAME")
ROBINHOOD_PASSWORD = getenv("ROBINHOOD_PASSWORD")
ALPHA_VANTAGE_API_KEY = getenv("ALPHA_VANTAGE_API_KEY")
STOCK_TAG = getenv("STOCK_TAG")
STOCK_MAX_PRICE = getenv("STOCK_MAX_PRICE")

#Set additional variables
mt_file = "monitored-tickers.csv"
monitored_tickers = []  # stocks to monitor
current_price = 0.0  # reset current_price variable on each run
share_qty = 1  # how many shares to buy/sell at a time
log_file = "/logs/transaction-log.csv"  # CSV to log output to
# CSV to store monitored tickers between each run
mt_file = "/logs/monitored-tickers.csv"


def append_ticker_to_csv(ticker):
    with open(mt_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ticker])

#log into Robinhood using credentials in the .env file
def rs_login():
    print("Logging you into: " + ROBINHOOD_USERNAME)
    login = robin_stocks.authentication.login(
        username=ROBINHOOD_USERNAME, password=ROBINHOOD_PASSWORD, store_session=True)

#query Robinhood for all stock tickers with a specified tag (eg. "technology") and
#update monitored-tickers.csv file with all stocks that have a value below ticker_max_price
def update_tickers_from_tag(tag, ticker_max_price):
    added_ticker_count = 0
    for stock in robin_stocks.get_all_stocks_from_market_tag(tag):
        if stock['symbol'] not in monitored_tickers:
            if float(stock['ask_price']) > 1.00 and float(stock['ask_price']) < ticker_max_price:
                append_ticker_to_csv(stock['symbol'])
                added_ticker_count += 1
    print("Added " + str(added_ticker_count) + " to " + mt_file)


#returns a date object given an original date and a delta (number of months) to add/subtract by
def find_month_delta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    return date.replace(month=m, year=y)


#function to plot data using matplotlib
def generate_plot(actual_data, day_ema, weekly_ema, ticker, action):
    #set graph's start and end dates
    # how many months before today to zoom graph into. Default is 18 months
    graph_months_before_today = 18
    # calculate the date when the graph starts plotting (minimum x). Default is 18 months before today's date
    graph_start_date = find_month_delta(date.today(), -graph_months_before_today)
    # calculate the date when the graph stops plotting (maximum x). Default is 1 month after today's date
    graph_end_date = find_month_delta(date.today(), 1)

    #axis setup
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    #add labels to axis
    plt.xlabel('date')
    plt.ylabel('price')

    #plot data
    actual_data['4. close'].plot(ax=ax, label='Actual Price')
    day_ema.plot(ax=ax, label='day ema')
    weekly_ema.plot(ax=ax, label='weekly ema')

    #set rotation of x axis labels to 90 degrees to more easily view the dates
    for label in ax.get_xticklabels():
        label.set_rotation(90)

    #graph settings
    plt.legend(loc='best')
    plt.title(ticker + " " + action + " " + str(date.today()))
    plt.grid()
    # zoom graph into more current data. This script collects stock data several years back, which we need to process but dont need to plot
    plt.xlim(graph_start_date, graph_end_date)
    plt.savefig("/logs/graph-exports/" + action + "-" + ticker + "-" +
                str(datetime.now())[:16].replace(':', '.') + ".png")  # exports graph to image
    #plt.show() #show interactive graph in popup window. This will hold up code execution until the graph window is exited
    plt.clf()  # clear plot so the script can reuse the same variables


#function to append data to CSV log
def append_to_log(action, status, ticker, current_price):
    with open(log_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([action, status, ticker, str(
            datetime.now()), str(current_price)])
        #Adding a print statement for now as Docker likes to use console
        print([action, status, ticker, str(datetime.now()), str(current_price)])


def populate_ticker():
    with open(mt_file, 'r') as ticker_file:
        csv_reader = csv.reader(ticker_file)
        for row in csv_reader:
            monitored_tickers.append(row[0])
    rs_login()
    update_tickers_from_tag(tag, STOCK_MAX_PRICE)

def main():
    #log start of daily run
    append_to_log("DAILY RUN", "STARTED", "N/A", "N/A")

    #load monitored stock tickers from CSV file
    with open(mt_file, 'r') as ticker_file:
        csv_reader = csv.reader(ticker_file)
        for row in csv_reader:
            monitored_tickers.append(row[0])

    #iterate through each ticker in array and run daily checks
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
        print("_____________________ " + ticker +
              " - [" + str(round(current_price, 2)) + "]")

        #get actual price
        actual_data, meta_data = ts.get_weekly(symbol=ticker)

        #get day ema
        day_ema, meta_deta = ti.get_ema(symbol=ticker, interval='daily')

        #get weekly ema
        weekly_ema, meta_deta = ti.get_ema(symbol=ticker, interval='weekly')

        for val in day_ema.iterrows():
            day_emas.append([val[0], val[1].values])
        for val in weekly_ema.iterrows():
            week_emas.append([val[0], val[1].values])

        for day in day_emas:
            for week in week_emas:
                if week[0] == day[0]:
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

        try:
            #if the latest buy trigger is today's date, place Robinhood order
            if str(date.today()) == str(buy_triggers[-1][0].to_pydatetime())[:10]:
                print("##### STOCK BUY HAS BEEN TRIGGERED #####")

                action = "BUY"

                append_to_log(action, "STARTED", ticker, current_price)

                #log into Robinhood
                rs_login()

                #plot data with matplotlib
                generate_plot(actual_data, day_ema, weekly_ema, ticker, action)

                #confirm action with user
                #prompt_user(action, ticker, current_price)

                #buy qty of specified stock from Robinhood
                try:
                    robin_stocks.order_buy_market(
                        ticker, share_qty)  # place the buy in Robinhood
                    append_to_log(action, "COMPLETED", ticker, current_price)
                except Exception as err:
                    print('Error ' + action.lower() + 'ing ' + ticker + ": " + err)
                    append_to_log(action, "ERROR: " + err, ticker, current_price)

            #if the latest sell trigger is today's date, sell shares of that stock
            elif str(date.today()) == str(sell_triggers[-1][0].to_pydatetime())[:10]:
                print("##### STOCK SELL HAS BEEN TRIGGERED #####")

                action = "SELL"

                append_to_log(action, "STARTED", ticker, current_price)

                #log into Robinhood
                rs_login()

                #plot data with matplotlib
                generate_plot(actual_data, day_ema, weekly_ema, ticker, action)

                #confirm action with user
                #prompt_user(action, ticker, current_price)

                #sell qty of specified stock from Robinhood
                try:
                    robin_stocks.order_sell_market(
                        ticker, share_qty)  # place the sell in Robinhood
                    append_to_log(action, "COMPLETED", ticker, current_price)
                except Exception as err:
                    print('Error ' + action.lower() + 'ing ' + ticker + ": " + err)
                    append_to_log(action, "ERROR: " + err, ticker, current_price)

        except Exception as err:
            print(err)

        #generate_plot(actual_data, day_ema, weekly_ema, ticker, "RUN")
        # sleep for a minute to wait out the query limit on the free AlphaVantage API
        time.sleep(60)

    #log completion of daily run
    append_to_log("DAILY RUN", "COMPLETED", "N/A", "N/A")


pd.set_option("display.max_rows", None, "display.max_columns", None)

#Alpha Vantage connection info
ts = TimeSeries(key='ALPHA_VANTAGE_API_KEY', output_format='pandas')
ti = TechIndicators(key='ALPHA_VANTAGE_API_KEY', output_format='pandas')
