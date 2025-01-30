# Python Script for TWS using ib_insync
# Python Version: 3.11 (latest stable version as of October 2023)

# Install necessary packages using the following commands:
# pip install ib_insync
# pip install pandas

from ib_insync import *
from ibapi.common import MarketDataTypeEnum

# Connect to TWS
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# Set market data type to DELAYED
ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)

# Define the stock contract for TREX on SMART exchange
contract = Stock('TREX', 'SMART', 'USD')

# Qualify the contract to ensure all details are filled
ib.qualifyContracts(contract)

# Print the contract ID
print(f"Contract ID: {contract.conId}")

# Request market data for the stock and print the price
ticker = ib.reqMktData(contract)
ib.sleep(2)  # Wait for data to arrive
print(f"Current price of TREX: {ticker.marketPrice()}")

# Request option chain for the stock
option_chains = ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)

# Extract and print expiration dates
expiration_dates = option_chains[0].expirations
print("Option Chain Expiration Dates:")
for date in expiration_dates:
    print(date)

# Print option chain (Call and Put) for each expiration date
for date in expiration_dates:
    print(f"\nExpiration Date: {date}")
    
    # Create call and put contracts
    call_contract = Option(contract.symbol, date, strike=0, right='C', exchange='SMART')
    put_contract = Option(contract.symbol, date, strike=0, right='P', exchange='SMART')
    
    # Qualify the contracts
    ib.qualifyContracts(call_contract)
    ib.qualifyContracts(put_contract)
    
    # Print call contract details
    print("Call Contract:")
    print(call_contract)
    
    # Print put contract details
    print("Put Contract:")
    print(put_contract)

# Disconnect from TWS
ib.disconnect()