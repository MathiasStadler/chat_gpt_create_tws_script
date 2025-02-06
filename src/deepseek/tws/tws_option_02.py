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
15. please use delayed market data use for that => ib.reqMarketDataType(MarketDataTypeEnum.DELAYED) , import for that from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum
16 please add the greeks delta, gama,vega and theta

"""


import os
import csv
from ib_insync import *
from ibapi.common import MarketDataTypeEnum

class OptionDataFetcher:
    def __init__(self, symbol):
        self.symbol = symbol
        self.ib = IB()
        self.connected = False

    def connect_to_ib(self):
        """Connect to Interactive Brokers TWS."""
        try:
            self.ib.connect('127.0.0.1', 7496, clientId=1)  # Paper account port
            self.ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)  # Use delayed market data
            self.connected = True
            print("Connected to Interactive Brokers TWS.")
        except Exception as e:
            print(f"Failed to connect to Interactive Brokers: {e}")
            self.connected = False

    def fetch_option_chain(self):
        """Fetch the option chain for the given symbol."""
        if not self.connected:
            print("Not connected to Interactive Brokers.")
            return None, None

        try:
            # Define the stock contract
            contract = Stock(self.symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)

            # Fetch option chains
            chains = self.ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)
            if not chains:
                print(f"No option chain found for {self.symbol}.")
                return None, None

            # Use the first expiry and strikes from the first chain
            chain = chains[0]
            expiry = chain.expirations[0]  # Use the first expiry date
            strikes = chain.strikes[:10]  # Limit to the first 10 strikes for efficiency

            # Create option contracts for calls and puts
            options = []
            for strike in strikes:
                call = Option(self.symbol, expiry, strike, 'C', 'SMART', 'USD')
                put = Option(self.symbol, expiry, strike, 'P', 'SMART', 'USD')
                options.extend([call, put])

            # Qualify and fetch tickers for the options
            self.ib.qualifyContracts(*options)
            tickers = self.ib.reqTickers(*options)

            # Extract mid and ask prices
            option_data = []
            for ticker in tickers:
                mid_price = (ticker.bid + ticker.ask) / 2 if ticker.bid and ticker.ask else None
                option_data.append({
                    'symbol': ticker.contract.symbol,
                    'strike': ticker.contract.strike,
                    'right': ticker.contract.right,
                    'mid_price': mid_price,
                    'ask_price': ticker.ask
                })

            return option_data, expiry

        except Exception as e:
            print(f"Error fetching option chain: {e}")
            return None, None

    def save_to_csv(self, data, expiry):
        """Save the option data to a CSV file without overwriting existing files."""
        if not data:
            print("No data to save.")
            return

        # Generate a unique filename
        base_filename = f"{self.symbol}_options_{expiry}.csv"
        filename = base_filename
        counter = 1
        while os.path.exists(filename):
            filename = f"{self.symbol}_options_{expiry}_{counter}.csv"
            counter += 1

        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['symbol', 'strike', 'right', 'mid_price', 'ask_price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Option data saved to {filename}.")
        except Exception as e:
            print(f"Error saving data to CSV: {e}")

    def print_option_data(self, data, expiry):
        """Print the option data in the specified format."""
        if not data:
            print("No option data to display.")
            return

        # Print the expiration date
        print(f"\nExpiration Date: {expiry}")
        print("Option Data:")
        print("Call Mid | Call Ask | Strike | Put Mid | Put Ask")
        print("-" * 50)

        # Group data by strike
        strike_data = {}
        for row in data:
            strike = row['strike']
            if strike not in strike_data:
                strike_data[strike] = {'call': None, 'put': None}
            if row['right'] == 'C':
                strike_data[strike]['call'] = row
            else:
                strike_data[strike]['put'] = row

        # Print formatted data
        for strike, values in sorted(strike_data.items()):
            call = values['call']
            put = values['put']
            call_mid = call['mid_price'] if call else 'N/A'
            call_ask = call['ask_price'] if call else 'N/A'
            put_mid = put['mid_price'] if put else 'N/A'
            put_ask = put['ask_price'] if put else 'N/A'
            print(f"{call_mid:>8} | {call_ask:>8} | {strike:>6} | {put_mid:>7} | {put_ask:>7}")

    def disconnect(self):
        """Disconnect from Interactive Brokers TWS."""
        if self.connected:
            try:
                self.ib.disconnect()
                print("Disconnected from Interactive Brokers TWS.")
            except Exception as e:
                print(f"Error disconnecting: {e}")
            finally:
                self.connected = False

def main():
    symbol = input("Enter the stock symbol (e.g., AAPL): ").strip().upper()
    if not symbol:
        print("No symbol provided. Exiting.")
        return

    fetcher = OptionDataFetcher(symbol)
    fetcher.connect_to_ib()

    try:
        option_data, expiry = fetcher.fetch_option_chain()
        if option_data:
            fetcher.save_to_csv(option_data, expiry)
            fetcher.print_option_data(option_data, expiry)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        fetcher.disconnect()

if __name__ == "__main__":
    main()