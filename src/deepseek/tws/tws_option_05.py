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
            print(f"Qualified stock contract: {contract}")

            # Fetch option chains
            chains = self.ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)
            if not chains:
                print(f"No option chain found for {self.symbol}.")
                return None, None

            # Log available expiry dates and strikes
            for i, chain in enumerate(chains):
                print(f"Chain {i + 1}: Expirations: {chain.expirations}, Strikes: {chain.strikes}")

            # Use the first expiry and strikes from the first chain
            chain = chains[0]
            expiry = chain.expirations[0]  # Use the first expiry date
            strikes = chain.strikes[:10]  # Limit to the first 10 strikes for efficiency
            print(f"Using expiry: {expiry}, strikes: {strikes}")

            # Create option contracts for calls and puts
            options = []
            for strike in strikes:
                call = Option(self.symbol, expiry, strike, 'C', 'SMART', 'USD')
                put = Option(self.symbol, expiry, strike, 'P', 'SMART', 'USD')
                options.extend([call, put])

            # Qualify and fetch tickers for the options
            qualified_contracts = self.ib.qualifyContracts(*options)
            print(f"Qualified option contracts: {qualified_contracts}")

            tickers = self.ib.reqTickers(*options)
            print(f"Fetched tickers: {tickers}")

            # Extract mid, ask prices, and Greeks
            option_data = []
            for ticker in tickers:
                mid_price = (ticker.bid + ticker.ask) / 2 if ticker.bid and ticker.ask else None
                option_data.append({
                    'symbol': ticker.contract.symbol,
                    'strike': ticker.contract.strike,
                    'right': ticker.contract.right,
                    'mid_price': mid_price,
                    'ask_price': ticker.ask,
                    'delta': ticker.modelGreeks.delta if ticker.modelGreeks else None,
                    'gamma': ticker.modelGreeks.gamma if ticker.modelGreeks else None,
                    'vega': ticker.modelGreeks.vega if ticker.modelGreeks else None,
                    'theta': ticker.modelGreeks.theta if ticker.modelGreeks else None
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
                fieldnames = ['symbol', 'strike', 'right', 'mid_price', 'ask_price', 'delta', 'gamma', 'vega', 'theta']
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
        print("Call Mid | Call Ask | Delta  | Gamma  | Vega   | Theta  | Strike | Put Mid | Put Ask | Delta  | Gamma  | Vega   | Theta")
        print("-" * 110)

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

            # Call data
            call_mid = call['mid_price'] if call and call['mid_price'] is not None else 'N/A'
            call_ask = call['ask_price'] if call and call['ask_price'] is not None else 'N/A'
            call_delta = call['delta'] if call and call['delta'] is not None else 'N/A'
            call_gamma = call['gamma'] if call and call['gamma'] is not None else 'N/A'
            call_vega = call['vega'] if call and call['vega'] is not None else 'N/A'
            call_theta = call['theta'] if call and call['theta'] is not None else 'N/A'

            # Put data
            put_mid = put['mid_price'] if put and put['mid_price'] is not None else 'N/A'
            put_ask = put['ask_price'] if put and put['ask_price'] is not None else 'N/A'
            put_delta = put['delta'] if put and put['delta'] is not None else 'N/A'
            put_gamma = put['gamma'] if put and put['gamma'] is not None else 'N/A'
            put_vega = put['vega'] if put and put['vega'] is not None else 'N/A'
            put_theta = put['theta'] if put and put['theta'] is not None else 'N/A'

            # Format the output
            print(f"{call_mid:>8} | {call_ask:>8} | {call_delta:>6} | {call_gamma:>6} | {call_vega:>6} | {call_theta:>6} | {strike:>6} | {put_mid:>7} | {put_ask:>7} | {put_delta:>6} | {put_gamma:>6} | {put_vega:>6} | {put_theta:>6}")

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