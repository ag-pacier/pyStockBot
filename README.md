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

Buy and sell triggers can be evaluated using this [calculator](https://dqydj.com/stock-return-calculator/) to view estimated returns if you had purchased a given stock on the date when the script triggered the buy/sell.

## Customization
Modify `monitored_tickers` array with the stocks you want to monitor for buy/sell triggers.

Set `store_session=True` in the Robinhood login calls to store your Robinhood account in the session header. This will remove the MFA prompt requirement when a buy or sell has been triggered, allowing the script to place the order without needing your MFA code for each action.

## Running
Run `trader.py` daily at 4:10PM EST. This can be accomplished with a cronjob or similar task, depending on your OS.

Example cronjob:
`40 6 * * * cd /path/to/project_folder/ && $(which python3) trader.py`