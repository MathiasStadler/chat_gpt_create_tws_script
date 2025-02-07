"""
Installation Instructions:
Run the following command to install required libraries:
    pip install yfinance pandas numpy
"""

import yfinance as yf
import pandas as pd
import numpy as np
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
        """Retrieve option chains that expire within the next 45 days along with Greeks and market data."""
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
                    calls = option_chain.calls
                    puts = option_chain.puts
                    
                    # Define required columns
                    required_columns = ['contractSymbol', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'impliedVolatility']
                    greek_columns = ['delta', 'theta', 'gamma', 'rho']
                    
                    # Check and include Greek columns only if they exist
                    for col in greek_columns:
                        if col in calls.columns:
                            required_columns.append(col)
                        if col in puts.columns:
                            required_columns.append(col)
                    
                    calls = calls[required_columns]
                    puts = puts[required_columns]
                    
                    # Add Delta Open Interest calculation if delta and openInterest exist
                    if 'delta' in calls.columns and 'openInterest' in calls.columns:
                        calls['deltaOI'] = calls['delta'] * calls['openInterest']
                    if 'delta' in puts.columns and 'openInterest' in puts.columns:
                        puts['deltaOI'] = puts['delta'] * puts['openInterest']
                    
                    option_data[expiry] = {
                        "calls": calls,
                        "puts": puts
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
