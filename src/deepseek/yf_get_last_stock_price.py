# deep seek prompt
"""
Create a script for use the Python Library Yahoo Finance API with the following characteristics
 1. get the stock name from the first argument by call the program
 2. get the last price of the stock
"""


# Python Script to Fetch the Last Price of a Stock Using Yahoo Finance API
# Python Version: 3.11 (latest stable version as of October 2023)

# Install necessary packages using the following commands:
# pip install yfinance

import sys
import yfinance as yf

# Check if a stock ticker is provided as an argument
if len(sys.argv) < 2:
    print("Usage: python get_stock_price.py <stock_ticker>")
    sys.exit(1)

# Get the stock ticker from the first argument
stock_ticker = sys.argv[1]

# Fetch the stock data
stock = yf.Ticker(stock_ticker)

# Get the last price (latest close price)
last_price = stock.history(period="1d")['Close'].iloc[-1]

# Print the last price
print(f"The last price of {stock_ticker} is: {last_price:.2f}")