# Python script to connect to TWS and get the price of TREX stock

# Import necessary packages
from ib_insync import *
from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum

# Display the Python version
import sys
print("Python version:", sys.version)

# Connect to TWS
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# Set market data type to delayed
ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)

# Create a stock contract for TREX
trex_contract = Stock('TREX', 'SMART', 'USD')

# Request market data for TREX
market_data = ib.reqMktData(trex_contract)

# Wait for the market data to be received
ib.sleep(2)

# Print the price of TREX
print("Price of TREX (delayed):", market_data.last)

# Disconnect from TWS
ib.disconnect()