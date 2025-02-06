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
"""

import os
import csv
from ib_insync import *
from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum

class OptionDataFetcher:
    def __init__(self, symbol):
        self.symbol = symbol
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7496, clientId=1)  # Paper account port
        self.ib.reqMarketDataType(MarketDataTypeEnum.DELAYED)  # Use delayed market data

    def fetch_option_chain(self):
        try:
            contract = Stock(self.symbol, 'SMART', 'USD')
            self.ib.qualifyContracts(contract)
            chains = self.ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)
            if not chains:
                print(f"No option chain found for {self.symbol}.")
                return None

            # Get the first option chain
            chain = chains[0]
            strikes = chain.strikes
            expiry = chain.expirations[0]  # Use the first expiry date

            options = []
            for strike in strikes:
                call = Option(self.symbol, expiry, strike, 'C', 'SMART', 'USD')
                put = Option(self.symbol, expiry, strike, 'P', 'SMART', 'USD')
                options.extend([call, put])

            self.ib.qualifyContracts(*options)
            tickers = self.ib.reqTickers(*options)

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

            return option_data

        except Exception as e:
            print(f"Error fetching option chain: {e}")
            return None

    def save_to_csv(self, data):
        if not data:
            return

        filename = f"{self.symbol}_options.csv"
        if os.path.exists(filename):
            base, ext = os.path.splitext(filename)
            i = 1
            while os.path.exists(f"{base}_{i}{ext}"):
                i += 1
            filename = f"{base}_{i}{ext}"

        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['symbol', 'strike', 'right', 'mid_price', 'ask_price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data to CSV: {e}")

    def print_option_data(self, data):
        if not data:
            return

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
        for strike, values in strike_data.items():
            call = values['call']
            put = values['put']
            call_mid = call['mid_price'] if call else 'N/A'
            call_ask = call['ask_price'] if call else 'N/A'
            put_mid = put['mid_price'] if put else 'N/A'
            put_ask = put['ask_price'] if put else 'N/A'
            print(f"{call_mid:>7} {call_ask:>7} | {strike:>7} | {put_mid:>7} {put_ask:>7}")

    def disconnect(self):
        try:
            self.ib.disconnect()
        except Exception as e:
            print(f"Error disconnecting: {e}")

def main():
    symbol = 'AAPL'  # Replace with your desired stock symbol
    fetcher = OptionDataFetcher(symbol)

    try:
        option_data = fetcher.fetch_option_chain()
        if option_data:
            fetcher.save_to_csv(option_data)
            fetcher.print_option_data(option_data)
    finally:
        fetcher.disconnect()

if __name__ == "__main__":
    main()