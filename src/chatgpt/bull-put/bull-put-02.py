"""

1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
7.use the Python Yahoo Finance API 
8 Create a list on start of the script with command how to install all necessary library
9.explain the option strategy bull put spread

"""


"""
Installation Instructions:
Run the following command to install required libraries:
    pip install yfinance pandas numpy
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

NASDAQ_100_TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "NVDA", "PEP", "AVGO", 
    "COST", "ADBE", "CSCO", "NFLX", "AMD", "INTC", "CMCSA", "TXN", "QCOM", "HON"
]

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
    
    def find_bull_put_spreads(self, expiry):
        """Identify potential Bull Put Spread opportunities."""
        try:
            option_chain = self.stock.option_chain(expiry)
            puts = option_chain.puts
            
            # Ensure required columns exist
            if not {'strike', 'bid', 'ask'}.issubset(puts.columns):
                print("Required columns missing in put options data.")
                return None
            
            puts = puts[['contractSymbol', 'strike', 'bid', 'ask']].sort_values(by='strike')
            spreads = []
            
            for i in range(len(puts) - 1):
                sell_put = puts.iloc[i]
                buy_put = puts.iloc[i + 1]
                
                credit = sell_put['bid'] - buy_put['ask']
                risk = buy_put['strike'] - sell_put['strike'] - credit
                
                if credit > 0 and risk > 0:
                    spreads.append({
                        'Sell Put Strike': sell_put['strike'],
                        'Buy Put Strike': buy_put['strike'],
                        'Credit Received': credit,
                        'Max Risk': risk,
                        'Risk-Reward Ratio': credit / risk if risk != 0 else None
                    })
            
            return spreads
        except Exception as e:
            print(f"Error identifying bull put spreads: {e}")
            return None
    
    @staticmethod
    def find_nasdaq_100_bull_put_spreads():
        """Find valid Bull Put Spreads for all NASDAQ-100 tickers."""
        results = {}
        for ticker in NASDAQ_100_TICKERS:
            finance = YahooFinanceOptions(ticker)
            options = finance.get_near_expiry_options()
            
            if options:
                for expiry in options.keys():
                    spreads = finance.find_bull_put_spreads(expiry)
                    if spreads:
                        results[ticker] = {expiry: spreads}
        
        return results

def main():
    """Main function to execute the script."""
    choice = input("Enter stock ticker or type 'NASDAQ100' to find spreads for NASDAQ-100: ")
    
    if choice.upper() == "NASDAQ100":
        results = YahooFinanceOptions.find_nasdaq_100_bull_put_spreads()
        for ticker, data in results.items():
            print(f"\nTicker: {ticker}")
            for expiry, spreads in data.items():
                print(f"Expiration Date: {expiry}")
                for spread in spreads:
                    print(spread)
    else:
        finance = YahooFinanceOptions(choice.upper())
        options = finance.get_near_expiry_options()
        
        if options:
            for expiry, data in options.items():
                print(f"\nExpiration Date: {expiry}")
                print("Calls:")
                print(data['calls'])
                print("Puts:")
                print(data['puts'])
                
                spreads = finance.find_bull_put_spreads(expiry)
                if spreads:
                    print("\nPotential Bull Put Spreads:")
                    for spread in spreads:
                        print(spread)
                else:
                    print("No valid Bull Put Spreads found.")
        else:
            print("No options retrieved.")

if __name__ == "__main__":
    main()
