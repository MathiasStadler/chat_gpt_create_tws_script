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
    "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "NVDA", "PEP", "AVGO", "COST", "ADBE", "CSCO", "NFLX", "AMD", "INTC", "CMCSA", "TXN", "QCOM", "HON", "PYPL", "AMGN", "SBUX", "ISRG", "ADI", "MDLZ", "GILD", "INTU", "BKNG", "ADP", "REGN", "VRTX", "LRCX", "ASML", "MRNA", "MU", "SNPS", "KDP", "MCHP", "CDNS", "PANW", "NXPI", "ORLY", "MAR", "ABNB", "FTNT", "CHTR", "KLAC", "PDD", "CTAS", "ROST", "MNST", "AZN", "PAYX", "ODFL", "WDAY", "BIIB", "XEL", "EXC", "CSX", "LULU", "DXCM", "PCAR", "IDXX", "MRVL", "GEHC", "VRSK", "ILMN", "CRWD", "CPRT", "AEP", "DLTR", "EBAY", "FAST", "GFS", "ZS", "ANSS", "SGEN", "SIRI", "TEAM", "CDW", "FISV", "WBA", "KHC", "CTSH", "CEG", "VRSN", "BIDU", "PPG", "ALGN", "ENPH", "DDOG", "PDD", "LNT", "BMRN", "MTCH", "TTD", "TTWO", "DOCU", "ZBRA", "BKR", "QRVO", "SWKS", "FOXA", "FOX"]

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
                    
                    calls = calls[required_columns].astype(float)
                    puts = puts[required_columns].astype(float)
                    
                    # Add Delta Open Interest calculation if delta and openInterest exist
                    if 'delta' in calls.columns and 'openInterest' in calls.columns:
                        calls['deltaOI'] = (calls['delta'] * calls['openInterest']).astype(float)
                    if 'delta' in puts.columns and 'openInterest' in puts.columns:
                        puts['deltaOI'] = (puts['delta'] * puts['openInterest']).astype(float)
                    
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
    
    @staticmethod
    def find_nasdaq_100_bull_put_spreads(min_rr, max_rr):
        """Find valid Bull Put Spreads for NASDAQ-100 stocks."""
        results = {}
        for ticker in NASDAQ_100_TICKERS:
            finance = YahooFinanceOptions(ticker)
            options = finance.get_near_expiry_options()
            if options:
                spreads = {}
                for expiry, data in options.items():
                    spread = finance.find_bull_put_spreads(expiry, min_rr, max_rr)
                    if spread:
                        spreads[expiry] = spread
                if spreads:
                    results[ticker] = spreads
        return results

def save_to_csv(data, ticker):
    """Save retrieved option data to a CSV file."""
    for expiry, contracts in data.items():
        filename = f"{ticker}_{expiry}.csv"
        df_calls = contracts["calls"]
        df_puts = contracts["puts"]
        
        df_calls["type"] = "call"
        df_puts["type"] = "put"
        
        df = pd.concat([df_calls, df_puts])
        df.to_csv(filename, index=False)
        print(f"Saved option data to {filename}")

def main():
    """Main function to execute the script."""
    choice = input("Enter stock ticker or type 'NASDAQ100' to find spreads for NASDAQ-100: ")
    min_rr = float(input("Enter minimum Risk-Reward Ratio: "))
    max_rr = float(input("Enter maximum Risk-Reward Ratio: "))
    
    if choice.upper() == "NASDAQ100":
        results = YahooFinanceOptions.find_nasdaq_100_bull_put_spreads(min_rr, max_rr)
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
            save_to_csv(options, choice.upper())
            for expiry, data in options.items():
                spreads = finance.find_bull_put_spreads(expiry, min_rr, max_rr)
                if spreads:
                    print(f"\nExpiration Date: {expiry}")
                    for spread in spreads:
                        print(spread)
                else:
                    print("No valid Bull Put Spreads found within the specified range.")
        else:
            print("No options retrieved.")

if __name__ == "__main__":
    main()
