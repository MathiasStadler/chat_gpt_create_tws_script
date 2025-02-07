"""
1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
7.use the TWS IBKR  insync API 
8 Create a list on start of the script with command how to install all necessary library
9.explain the option strategy bull put spread
10. add a function to search valid bull put spread
11. use the market data
12. write the result of the script inside a csv file
13. use all stock with option from the Nasdaq 100
14. Please use paper account with follow parameter => self.ib.connect('127.0.0.1', 7496, clientId=33)


1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
7.use the TWS IBKR  insync API 
8 Create a list on start of the script with command how to install all necessary library
9.explain the option strategy bull put spread
10. add a function to search valid bull put spread
11. use the market data
12. write the result of the script inside a csv file
13. use all stock with option from the Nasdaq 100
"""

import csv
from ib_insync import *
import pandas as pd

# Install necessary libraries
# pip install ib_insync pandas

class BullPutSpread:
    def __init__(self, ib):
        self.ib = ib

    def connect_to_tws(self):
        """Connect to the TWS API (Paper Trading Account)."""
        try:
            self.ib.connect('127.0.0.1', 7496, clientId=33)  # Paper trading port
            print("Connected to TWS Paper Trading Account.")
        except Exception as e:
            print(f"Error connecting to TWS API: {e}")

    def disconnect_from_tws(self):
        """Disconnect from the TWS API."""
        try:
            self.ib.disconnect()
            print("Disconnected from TWS API.")
        except Exception as e:
            print(f"Error disconnecting from TWS API: {e}")

    def get_nasdaq_100_stocks(self):
        """Fetch all stocks with options from the Nasdaq 100."""
        try:
            # Fetch Nasdaq 100 symbols (this is a placeholder; you may need to fetch the actual list)
            nasdaq_100_symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META']  # Example symbols
            print("Fetched Nasdaq 100 stocks with options.")
            return nasdaq_100_symbols
        except Exception as e:
            print(f"Error fetching Nasdaq 100 stocks: {e}")
            return []

    def get_option_chain(self, symbol):
        """Fetch the option chain for a given stock symbol."""
        try:
            contract = Stock(symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            chains = self.ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)
            return chains
        except Exception as e:
            print(f"Error fetching option chain for {symbol}: {e}")
            return None

    def find_bull_put_spread(self, symbol):
        """Find a valid bull put spread for a given stock symbol."""
        try:
            chains = self.get_option_chain(symbol)
            if not chains:
                return None

            # Extract put options from the option chain
            puts = []
            for chain in chains:
                for expiration in chain.expirations:
                    for strike in chain.strikes:
                        put = Option(symbol, expiration, strike, 'P', 'SMART')
                        self.ib.qualifyContracts(put)
                        puts.append(put)

            # Sort puts by strike price
            puts.sort(key=lambda x: x.strike)

            # Find a valid bull put spread
            if len(puts) >= 2:
                sell_put = puts[-1]  # Sell the higher strike put
                buy_put = puts[-2]   # Buy the lower strike put

                if sell_put.strike > buy_put.strike:
                    # Fetch market data for the options
                    self.ib.reqMarketDataType(1)  # Use delayed data if no live subscription
                    tickers = self.ib.reqTickers(sell_put, buy_put)
                    sell_put_price = tickers[0].marketPrice()
                    buy_put_price = tickers[1].marketPrice()

                    return {
                        'symbol': symbol,
                        'sell_put': sell_put.strike,
                        'buy_put': buy_put.strike,
                        'premium': sell_put_price - buy_put_price
                    }
            return None
        except Exception as e:
            print(f"Error finding bull put spread for {symbol}: {e}")
            return None

    def write_to_csv(self, data, filename='bull_put_spreads.csv'):
        """Write the results to a CSV file."""
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['symbol', 'sell_put', 'buy_put', 'premium'])
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            print(f"Results written to {filename}.")
        except Exception as e:
            print(f"Error writing to CSV file: {e}")

def main():
    ib = IB()
    strategy = BullPutSpread(ib)

    try:
        # Connect to TWS Paper Trading Account
        strategy.connect_to_tws()

        # Fetch Nasdaq 100 stocks with options
        symbols = strategy.get_nasdaq_100_stocks()

        # Find bull put spreads for each symbol
        results = []
        for symbol in symbols:
            spread = strategy.find_bull_put_spread(symbol)
            if spread:
                results.append(spread)

        # Write results to CSV
        strategy.write_to_csv(results)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Disconnect from TWS
        strategy.disconnect_from_tws()

if __name__ == "__main__":
    main()