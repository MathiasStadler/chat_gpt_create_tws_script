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
10. get the user portfolio data

"""

"""
Installation Instructions:
Run the following command to install necessary libraries:

pip install ib-insync pandas

"""

"""
Installation Instructions:
Run the following command to install necessary libraries:

pip install ib-insync pandas

"""

import os
import pandas as pd
from ib_insync import IB, Stock, Contract, util


class PortfolioManager:
    def __init__(self, host='127.0.0.1', port=7497, client_id=1):
        self.ib = IB()
        try:
            self.ib.connect(host, 7496, client_id)
            self.ib.reqMarketDataType(1)  # Use paper account market data
            print("Connected to Interactive Brokers Paper Account")
        except Exception as e:
            print(f"Connection error: {e}")

    def get_portfolio(self):
        try:
            portfolio = self.ib.portfolio()
            return portfolio
        except Exception as e:
            print(f"Error fetching portfolio: {e}")
            return []

    def fetch_stock_data(self, symbol):
        try:
            contract = Stock(symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            bars = self.ib.reqHistoricalData(
                contract,
                endDateTime='',
                durationStr='1 D',
                barSizeSetting='1 hour',
                whatToShow='MIDPOINT',
                useRTH=True,
                formatDate=1
            )
            return util.df(bars)
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return pd.DataFrame()

    def save_to_csv(self, symbol, data):
        try:
            filename = f"{symbol}.csv"
            counter = 1
            while os.path.exists(filename):
                filename = f"{symbol}_{counter}.csv"
                counter += 1
            data.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def close_connection(self):
        try:
            self.ib.disconnect()
            print("Disconnected from Interactive Brokers")
        except Exception as e:
            print(f"Error disconnecting: {e}")


def main():
    manager = PortfolioManager()
    portfolio = manager.get_portfolio()

    if not portfolio:
        print("No portfolio data found.")
    else:
        for position in portfolio:
            symbol = position.contract.symbol
            print(f"Fetching data for {symbol}")
            data = manager.fetch_stock_data(symbol)
            if not data.empty:
                manager.save_to_csv(symbol, data)

    manager.close_connection()


if __name__ == "__main__":
    main()

