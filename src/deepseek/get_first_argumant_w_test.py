# Python Script to Fetch Stock Data Using Yahoo Finance API
# Python Version: 3.11 (latest stable version as of October 2023)

# Install necessary packages using the following commands:
# pip install yfinance

import sys
import yfinance as yf

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_last_price(self):
        """Fetch the last price (latest close price) of the stock."""
        try:
            history = self.stock.history(period="1d")
            if history.empty:
                raise ValueError(f"No data found for ticker: {self.ticker}")
            last_price = history['Close'].iloc[-1]
            return last_price
        except Exception as e:
            print(f"Error fetching last price for {self.ticker}: {e}")
            return None

    def get_stock_info(self):
        """Fetch basic stock information."""
        try:
            info = self.stock.info
            return info
        except Exception as e:
            print(f"Error fetching stock info for {self.ticker}: {e}")
            return None

def main():
    # Check if at least one argument is provided (excluding the script name)
    if len(sys.argv) < 2:
        print("Error: No argument provided.")
        print("Usage: python script.py <stock_ticker>")
        sys.exit(1)

    # Get the first argument (stock ticker)
    stock_ticker = sys.argv[1]
    print(f"The first argument is: {stock_ticker}")

    # Create an instance of StockData
    stock_data = StockData(stock_ticker)

    # Fetch and print the last price
    last_price = stock_data.get_last_price()
    if last_price:
        print(f"The last price of {stock_ticker} is: {last_price:.2f}")

    # Fetch and print basic stock info
    stock_info = stock_data.get_stock_info()
    if stock_info:
        print(f"\nBasic info for {stock_ticker}:")
        for key, value in stock_info.items():
            print(f"{key}: {value}")

def run_tests():
    """Run test cases for the StockData class."""
    print("\nRunning test cases...")

    # Test case 1: Valid stock ticker
    print("\nTest Case 1: Valid stock ticker (AAPL)")
    stock_data = StockData("AAPL")
    last_price = stock_data.get_last_price()
    assert last_price is not None, "Test Case 1 Failed: No last price returned."
    print(f"Last price of AAPL: {last_price:.2f}")

    # Test case 2: Invalid stock ticker
    print("\nTest Case 2: Invalid stock ticker (INVALID_TICKER)")
    stock_data = StockData("INVALID_TICKER")
    last_price = stock_data.get_last_price()
    assert last_price is None, "Test Case 2 Failed: Last price should be None for invalid ticker."
    print("Last price of INVALID_TICKER: None (as expected)")

    # Test case 3: Fetch stock info
    print("\nTest Case 3: Fetch stock info (MSFT)")
    stock_data = StockData("MSFT")
    stock_info = stock_data.get_stock_info()
    assert stock_info is not None, "Test Case 3 Failed: No stock info returned."
    print("Stock info for MSFT fetched successfully.")

    print("\nAll test cases passed!")

if __name__ == "__main__":
    # Run the main function
    main()

    # Uncomment the following line to run test cases
    run_tests()