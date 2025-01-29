# Python script to connect to TWS and fetch the price of TREX stock

# Import necessary packages
from ib_insync import *
from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum
# Display the Python version
import sys
print("Python version:", sys.version)

# Install necessary packages (run this in your terminal)
# pip install ib-insync

# Connect to TWS
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# Define the stock symbol and market data type
symbol = 'TREX'
market_data_type = MarketDataTypeEnum.DELAYED

# Set market data type to delayed
ib.reqMarketDataType(market_data_type)

# Create a stock contract for TREX
contract = Stock(symbol, 'SMART', 'USD')

# Request market data
ib.reqMktData(contract)

# Sleep for a moment to allow data to be received
ib.sleep(2)

# Fetch and print the price
market_data = ib.ticker(contract)
print(f"The delayed price of {symbol} is: {market_data}")

# Disconnect from TWS
ib.disconnect()