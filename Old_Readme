# Python Stock Trader
## Getting Started
Install requirements: 
```
pip3 install -r requirements.txt
```

Create a file called `.env` in the same directory as your Python script and populate it with your passwords, API keys, and other secrets:
```
ROBINHOOD_USERNAME=alan@none.com
ROBINHOOD_PASSWORD=SuperSecurePassword!
ALPHA_VANTAGE_API_KEY=1a2s3d4f5g6h7j8k9l
```

Make sure `.env` is listed in your `.gitignore` file to ensure the file with environment variables doesn’t get uploaded to GitHub or other source control.

## Testing
Test the script with: `python3 trader.py`.

Buy triggers can be evaluated using this [calculator](https://dqydj.com/stock-return-calculator/) to view estimated returns if you had purchased a given stock on the date when the script triggered the buy.

## Customization
Run `populate-tickers.py` to specify criteria for monitored stocks and add them to a CSV that `trader.py` reads from to populate the `monitored_tickers` array with the stocks you want to monitor for buy/sell triggers.

Set `store_session=True` in the Robinhood login calls to store your Robinhood account in the session header. This will remove the MFA prompt requirement when a buy or sell has been triggered, allowing the script to place the order without needing your MFA code for each action.

## Running
Run `trader.py` daily at 4:10PM EST. This is shortly after the market closes for the day. This can be accomplished with a cronjob or similar task, depending on your OS.

Example cronjob:
`10 16 * * * cd /path/to/project_folder/ && $(which python3) trader.py`

## Notes
> By now I have pretty much abandoned this project, as stocks and finance are not really my passion; this was mainly a project to quickly teach a friend how to properly use environment variables, and I got interested in building the algorithm he was describing. A lot of the building blocks for EMA/SMA crossover event handling and using the Robinhood API are here, so I hope someone out there can get some use out of this or at least use it as a reference to build something cool.

~~This project is currently in the testing phase. My current setup is a Raspberry Pi 3 running this script via a cronjob every day.~~

If you plan on deploying this script to a Mac environment, you may have an issue with the access control mechanism that was introduced in Mojave where cron jobs can no longer access certain directories because they hold sensitive data. You can fix this by following the instructions on this [link](https://blog.bejarano.io/fixing-cron-jobs-in-mojave/). Be sure to understand the security concerns associated with this, and modify your environment accordingly.