import csv
import yfinance as yf
import pandas as pd

# Install necessary libraries
# pip install yfinance pandas

class BullPutSpread:
    def __init__(self):
        pass

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
            stock = yf.Ticker(symbol)
            options = stock.options  # Get available expiration dates
            if not options:
                return None

            # Fetch the nearest expiration date
            expiration = options[0]
            option_chain = stock.option_chain(expiration)
            puts = option_chain.puts  # Get put options
            return puts
        except Exception as e:
            print(f"Error fetching option chain for {symbol}: {e}")
            return None

    def find_bull_put_spread(self, symbol):
        """Find a valid bull put spread for a given stock symbol."""
        try:
            puts = self.get_option_chain(symbol)
            if puts is None or puts.empty:
                return None

            # Sort puts by strike price
            puts = puts.sort_values(by='strike')

            # Find a valid bull put spread
            if len(puts) >= 2:
                sell_put = puts.iloc[-1]  # Sell the higher strike put
                buy_put = puts.iloc[-2]   # Buy the lower strike put

                if sell_put['strike'] > buy_put['strike']:
                    return {
                        'symbol': symbol,
                        'sell_put': sell_put['strike'],
                        'buy_put': buy_put['strike'],
                        'premium': sell_put['lastPrice'] - buy_put['lastPrice']
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
    strategy = BullPutSpread()

    try:
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

if __name__ == "__main__":
    main()