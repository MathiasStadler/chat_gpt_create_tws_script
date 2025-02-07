"""
1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
7.use the Python Yahoo Finance API 
8 Create a list on start of the script with command how to install all necessary library
9.retrieve the option chain with expired date from max 45 day

"""

"""
Installation Instructions:
Run the following command to install required libraries:
    pip install yfinance pandas
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

class YahooFinanceOptions:
    def __init__(self, ticker):
        """Initialize with the stock ticker"""
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
    
    def get_option_expirations(self):
        """Retrieve available expiration dates for the options."""
        try:
            expirations = self.stock.options
            return expirations
        except Exception as e:
            print(f"Error retrieving expiration dates: {e}")
            return []
    
    def get_near_expiry_options(self):
        """Retrieve option chains that expire within the next 45 days."""
        try:
            expirations = self.get_option_expirations()
            if not expirations:
                return None
            
            # Filter expirations within 45 days
            max_date = datetime.today() + timedelta(days=45)
            valid_expirations = [date for date in expirations if datetime.strptime(date, "%Y-%m-%d") <= max_date]
            
            if not valid_expirations:
                print("No options available within the next 45 days.")
                return None
            
            option_data = {}
            for expiry in valid_expirations:
                try:
                    option_chain = self.stock.option_chain(expiry)
                    option_data[expiry] = {
                        "calls": option_chain.calls,
                        "puts": option_chain.puts
                    }
                except Exception as e:
                    print(f"Error retrieving option chain for {expiry}: {e}")
            
            return option_data
        except Exception as e:
            print(f"Error processing option chains: {e}")
            return None

def main():
    """Main function to execute the script."""
    ticker = input("Enter stock ticker: ")
    finance = YahooFinanceOptions(ticker)
    options = finance.get_near_expiry_options()
    
    if options:
        for expiry, data in options.items():
            print(f"\nExpiration Date: {expiry}")
            print("Calls:")
            print(data['calls'])
            print("Puts:")
            print(data['puts'])
    else:
        print("No options retrieved.")

if __name__ == "__main__":
    main()
