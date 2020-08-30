# Python Stock Trader
Create a file called `.env` in the same directory as your Python script and populate it with your passwords, API keys, and other secrets:
```
ROBINHOOD_USERNAME=alan@none.com
ROBINHOOD_PASSWORD=SuperSecurePassword!
ALPHA_VANTAGE_API_KEY=1a2s3d4f5g6h7j8k9l
```

Make sure to list `.env` in your `.gitignore` file to ensure the file with environment variables doesn’t get uploaded to GitHub.

Run the script with: `python3 trader.py`