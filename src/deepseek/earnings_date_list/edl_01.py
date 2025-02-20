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

# Installation Instructions:
# Run the following commands to install the required libraries:
# pip install ib_insync pandas

import sys
import csv
from ib_insync import *
import pandas as pd
from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum

# Define the MarketDataFetcher class
class MarketDataFetcher:
    def __init__(self, ib):
        self.ib = ib

    def get_market_data(self, symbol):
        """Fetch market data for a given symbol."""
        try:
            contract = Stock(symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            market_data = self.ib.reqMktData(contract, '', False, False)
            self.ib.sleep(2)  # Wait for data to populate
            return market_data
        except Exception as e:
            print(f"Error fetching market data for {symbol}: {e}")
            return None

    def get_earnings_dates(self, symbol):
        """Fetch upcoming earnings dates for a given symbol."""
        try:
            contract = Stock(symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            earnings = self.ib.reqFundamentalData(contract, 'REPORTS_FINANCIALS')
            return earnings
        except Exception as e:
            print(f"Error fetching earnings dates for {symbol}: {e}")
            return None

    def save_to_csv(self, data, filename='market_data_results.csv'):
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

        # Initialize MarketDataFetcher
        fetcher = MarketDataFetcher(ib)

        # Example symbol
        symbol = 'AAPL'

        # Fetch market data
        market_data = fetcher.get_market_data(symbol)
        if market_data:
            print(f"Market Data for {symbol}: {market_data}")

        # Fetch upcoming earnings dates
        earnings = fetcher.get_earnings_dates(symbol)
        if earnings:
            print(f"Upcoming Earnings Dates for {symbol}: {earnings}")

        # Save results to CSV
        results = [
            {
                'symbol': symbol,
                'market_data': market_data,
                'earnings_dates': earnings
            }
        ]
        fetcher.save_to_csv(results)

    except Exception as e:
        print(f"Error in main function: {e}")
    finally:
        # Disconnect from TWS
        ib.disconnect()

if __name__ == "__main__":
    main()