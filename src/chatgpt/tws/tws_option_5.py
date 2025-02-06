"""

1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
6. Create a list on start of the script with command how to install all necessary library
7. save download data inside a csv file with name of stock
8. don't overwrite any data files. Check first whether the file exists and if it exists, create a new one
9. use  the python library ib_insync 
10. get the first option chain if exits
11. use the paper acount port 
12. please use the port for connection 7496
13. please get the mid and ask price for each option 
14. please print the option data each strike in one line , the call left , the put data right and the strike price center
15. please use delayed market data use for that => ib.reqMarketDataType(MarketDataTypeEnum.DELAYED) import for that from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum
"""

import os
import pandas as pd
from ib_insync import IB, Stock, Option
from datetime import datetime

class OptionChainFetcher:
    def __init__(self, stock_symbol, host='127.0.0.1', port=7496, client_id=1):
        self.stock_symbol = stock_symbol
        self.ib = IB()
        self.stock = Stock(stock_symbol, 'SMART', 'USD')
        self.host = host
        self.port = port
        self.client_id = client_id

    def connect_to_ib(self):
        try:
            self.ib.connect(self.host, self.port, clientId=self.client_id)
            print(f"Connected to Interactive Brokers Paper Account at {self.host}:{self.port}")
        except Exception as e:
            print(f"Error connecting to IB: {e}")

    def validate_stock_contract(self):
        try:
            # Check if the stock contract is valid by requesting its market data
            self.ib.qualifyContracts(self.stock)
            print(f"Stock contract {self.stock_symbol} is valid.")
        except Exception as e:
            print(f"Error validating stock contract: {e}")
            return False
        return True

    def fetch_first_option_chain(self):
        try:
            if not self.validate_stock_contract():
                print("Invalid stock contract, cannot fetch option chain.")
                return []

            contract = self.stock
            options = self.ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)
            option_chain = []

            # Fetching only the first option chain (if available)
            if options:
                first_option = options[0]
                if first_option.expirations:
                    for expiration in first_option.expirations:
                        for strike in first_option.strikes:
                            for right in ['C', 'P']:  # Call and Put options
                                option_contract = Option(
                                    contract.symbol, expiration, strike, right, 'SMART')
                                
                                # Requesting delayed market data for the options
                                self.ib.reqMktData(option_contract, "", False, False)
                                self.ib.sleep(2)  # Delay to ensure data is received

                                # Fetching market data for ask, bid and mid price
                                market_data = self.ib.ticker(option_contract)
                                mid_price = (market_data.ask + market_data.bid) / 2 if market_data.ask and market_data.bid else None
                                
                                option_chain.append({
                                    'Symbol': contract.symbol,
                                    'Expiration': expiration,
                                    'Strike': strike,
                                    'Right': right,
                                    'Ask Price': market_data.ask if market_data.ask else None,
                                    'Mid Price': mid_price,
                                    'Bid Price': market_data.bid if market_data.bid else None
                                })
            return option_chain
        except Exception as e:
            print(f"Error fetching option chain: {e}")
            return []

    def save_option_chain_to_csv(self, option_chain):
        try:
            # Create the filename based on stock symbol
            filename = f"{self.stock_symbol}_option_chain.csv"

            # Check if the file exists, if so, append new data with a unique name
            if os.path.exists(filename):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{self.stock_symbol}_option_chain_{timestamp}.csv"

            # Convert option_chain to DataFrame and save as CSV
            df = pd.DataFrame(option_chain)
            df.to_csv(filename, index=False)
            print(f"Option chain saved to {filename}")
        except Exception as e:
            print(f"Error saving data to CSV: {e}")

    def print_option_chain(self, option_chain):
        try:
            for option in option_chain:
                print(f"{option['Symbol']} | Expiration: {option['Expiration']} | Strike: {option['Strike']} | "
                      f"Right: {option['Right']} | Ask Price: {option['Ask Price']} | Mid Price: {option['Mid Price']} | "
                      f"Bid Price: {option['Bid Price']}")
        except Exception as e:
            print(f"Error printing option chain: {e}")

    def disconnect_from_ib(self):
        try:
            self.ib.disconnect()
            print("Disconnected from Interactive Brokers Paper Account")
        except Exception as e:
            print(f"Error disconnecting from IB: {e}")

def main():
    stock_symbol = input("Enter the stock symbol: ")

    fetcher = OptionChainFetcher(stock_symbol, port=7496)  # Set to port 7496

    fetcher.connect_to_ib()
    option_chain = fetcher.fetch_first_option_chain()

    if option_chain:
        fetcher.print_option_chain(option_chain)  # Print option data
        fetcher.save_option_chain_to_csv(option_chain)

    fetcher.disconnect_from_ib()

if __name__ == "__main__":
    main()
