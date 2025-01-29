# Python script to connect to TWS and retrieve stock and option data
# Python version: 3.x (latest stable version)

# Install necessary packages
# pip install ib-insync

from ib_insync import *
from ibapi.common import MarketDataTypeEnum

# Connect to TWS
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# Set market data type to delayed
ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)

# Define the stock contract for TREX
stock_contract = Stock('TREX', 'SMART', 'USD')

# Qualify the contract
qualified_contracts = ib.qualifyContracts(stock_contract)


if not qualified_contracts:
    print("No qualified contracts found.")
else:
    stock_contract = qualified_contracts[0]

    # Request market data
    ib.reqMktData(stock_contract, '', False, False)

    # Print the price of the stock
    print(f"Price of {stock_contract.symbol}: {stock_contract.strike}")

    # Print the contract ID
    print(f"Contract ID: {stock_contract.conId}")

    # Retrieve option chain
    option_chain = ib.reqSecDefOptParams(stock_contract.symbol, '', stock_contract.secType, stock_contract.conId)

    # chains = ib.reqSecDefOptParams(spx.symbol, '', stock_contract.secType, stock_contract.conId)
    
    print(option_chain)

    # # Print expiration dates and option chains
    # for option in option_chain:
    #     print(f"Expiration Date: {option.expirations}")
    #     for expiration in option.expirations:
    #         # Request options for each expiration date
    #         options = ib.reqContractDetails(Option(stock_contract.symbol, expiration, 'C', stock_contract.exchange))
    #         print(f"Call Options for {expiration}: {[opt.contract.conId for opt in options]}")
    #         # options = ib.reqContractDetails(Option(stock_contract.symbol, expiration, 'P', stock_contract.exchange))
    #         # print(f"Put Options for {expiration}: {[opt.contract.conId for opt in options]}")

# Disconnect from TWS
ib.disconnect()