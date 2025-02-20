"""
1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
7.use the TWS IBKR  insync API 
8 Create a list on start of the script with command how to install all necessary library
9. use the market data
10. write the result of the script inside a csv file
11. get all next upcoming earnings date with quote
12. please use the paper account on localhost 127.0.0.1 with port 7496 and session id 33)
13, please use market_data_type = MarketDataTypeEnum.DELAYED
14. set market data type to delayed - ib.reqMarketDataType(market_data_type)
15. please add to the imports => from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum
"""


# https://www.google.com/search?client=firefox-b-e&channel=entpr&q=ibkr+api+get+earnings+data

# Installation Instructions:
# Run the following commands to install the required libraries:
# pip install ib_insync pandas

import sys
import csv
from ib_insync import *
import pandas as pd
from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum

# Define the FundamentalDataFetcher class
class FundamentalDataFetcher:
    def __init__(self, ib):
        self.ib = ib

    def get_fundamental_data(self, symbol, report_type='ReportsFinSummary'):
        """Fetch fundamental data for a given symbol."""
        try:
            contract = Stock(symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            fundamental_data = self.ib.reqFundamentalData(contract, report_type)
            return fundamental_data
        except Exception as e:
            print(f"Error fetching fundamental data for {symbol}: {e}")
            return None

    def save_to_csv(self, data, filename='fundamental_data_results.csv'):
        """Save results to a CSV file."""
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

# Main function
def main():
    try:
        # Connect to TWS paper account
        ib = IB()
        ib.connect('127.0.0.1', 7496, clientId=33)

        # Set market data type to DELAYED
        market_data_type = MarketDataTypeEnum.DELAYED
        ib.reqMarketDataType(market_data_type)
        print(f"Market data type set to: {market_data_type}")

        # Initialize FundamentalDataFetcher
        fetcher = FundamentalDataFetcher(ib)

        # Load NASDAQ stock symbols (example: use a CSV file or API)
        # Replace this with your method to get NASDAQ symbols
        nasdaq_symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA']  # Example symbols

        # Fetch fundamental data for each symbol
        results = []
        for symbol in nasdaq_symbols:
            print(f"Fetching fundamental data for {symbol}...")
            fundamental_data = fetcher.get_fundamental_data(symbol)
            if fundamental_data:
                results.append({
                    'symbol': symbol,
                    'fundamental_data': fundamental_data
                })
            else:
                print(f"No fundamental data available for {symbol}.")

        # Save results to CSV
        if results:
            fetcher.save_to_csv(results)
        else:
            print("No fundamental data fetched.")

    except Exception as e:
        print(f"Error in main function: {e}")
    finally:
        # Disconnect from TWS
        ib.disconnect()

if __name__ == "__main__":
    main()