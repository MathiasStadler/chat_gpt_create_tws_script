# Python script to connect to TWS and print the price of TREX stock

# Python version
import sys
print("Python version:", sys.version)

# Install necessary packages
# You can run the following command in your terminal to install ib-insync
# pip install ib-insync

from ib_insync import *
from ibapi.common import MarketDataTypeEnum

# Connect to TWS
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)
ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)

# Define the stock symbol for TREX
symbol = 'TREX'
exchange = 'NASDAQ'

# Create a stock contract
contract = Stock(symbol, exchange, 'USD')

# Request market data
ib.reqMktData(contract)

# Sleep for a moment to allow data to be received
ib.sleep(2)

# Print the price of the stock
market_data = ib.ticker(contract)
print(f"The current price of {symbol} on {exchange} is: {market_data.last}")

# Disconnect from TWS
ib.disconnect()