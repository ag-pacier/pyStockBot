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

Make sure `.env` is listed in your `.gitignore` file to ensure the file with environment variables doesn’t get uploaded to GitHub.

Modify `monitored_tickers` array with the stocks you want to monitor for buy/sell triggers.

## Testing
Test the script with: `python3 trader.py`.

## Running
Run `trader.py` daily at 4:10PM EST. This can be accomplished with a cronjob or similar task, depending on your OS.

Example cronjob:
`40 6 * * * cd /path/to/project_folder/ && $(which python3) trader.py`