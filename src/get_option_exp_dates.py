# Python version: 3.x (latest stable version as of January 2025)

# Install necessary packages
# You can install the required packages using the following commands:
# pip install ib-insync

from ib_insync import *
from ibapi.common import MarketDataTypeEnum

# Connect to TWS
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# Define the stock contract for TREX
contract = Stock('TREX', 'SMART', 'USD')

# Request market data
ib.reqMktData(contract, '', False, False)

# Wait for the market data to be received
ib.sleep(1)

# Print the price of the stock
print(f"Price of TREX: {contract.last()}")

# Print the contract ID
print(f"Contract ID: {contract.conId}")

# Request option chain for TREX
option_chain = ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)

# Print option chain expiration dates
print("Option Chain Expiration Dates:")
for option in option_chain:
    for expiration in option.expirations:
        print(expiration)

# Disconnect from TWS
ib.disconnect()