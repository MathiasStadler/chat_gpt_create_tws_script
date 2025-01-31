# Python script to connect to TWS and retrieve stock information
# Python version: 3.x (latest stable version as of January 2025)

# Install necessary packages
# pip install ib-insync

from ib_insync import *
from ibapi.common import MarketDataTypeEnum

# Connect to TWS
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# Define the stock contract for TREX
contract = Stock('TREX', 'SMART', 'USD')

# Qualify the contract to get the full details
qualified_contract = ib.qualifyContracts(contract)[0]

# Set market data type to delayed
ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)

# Request market data
market_data = ib.reqMktData(qualified_contract)

# Wait for the market data to be received
ib.sleep(1)

# Print the price and contract ID
print(f"Price of TREX: {market_data.last}")
print(f"Contract ID: {qualified_contract.conId}")

# Request option chain for TREX
option_chain = ib.reqSecDefOptParams(qualified_contract.symbol, '', qualified_contract.secType, qualified_contract.conId)

# Print option chain expiration dates
print("Option Chain Expiration Dates:")
for option in option_chain:
    print(option.expirations)

# Disconnect from TWS
ib.disconnect()
