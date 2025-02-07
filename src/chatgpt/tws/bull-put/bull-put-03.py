"""
Installation Instructions:
Run the following command to install required libraries:
    pip install ib_insync pandas numpy
"""

from ib_insync import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Connect to IBKR Paper Account
IB_PORT = 7496
ib = IB()
ib.connect('127.0.0.1', IB_PORT, clientId=1)

NASDAQ_100_TICKERS = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "NVDA", "PEP", "AVGO", "COST", "ADBE", "CSCO", "NFLX", "AMD", "INTC", "CMCSA", "TXN", "QCOM", "HON", "PYPL", "AMGN", "SBUX", "ISRG", "ADI", "MDLZ", "GILD", "INTU", "BKNG", "ADP", "REGN", "VRTX", "LRCX", "ASML", "MRNA", "MU", "SNPS", "KDP", "MCHP", "CDNS", "PANW", "NXPI", "ORLY", "MAR", "ABNB", "FTNT", "CHTR", "KLAC", "PDD", "CTAS", "ROST", "MNST", "AZN", "PAYX", "ODFL", "WDAY", "BIIB", "XEL", "EXC", "CSX", "LULU", "DXCM", "PCAR", "IDXX", "MRVL", "GEHC", "VRSK", "ILMN", "CRWD", "CPRT", "AEP", "DLTR", "EBAY", "FAST", "GFS", "ZS", "ANSS", "SGEN", "SIRI", "TEAM", "CDW", "FISV", "WBA", "KHC", "CTSH", "CEG", "VRSN", "BIDU", "PPG", "ALGN", "ENPH", "DDOG", "PDD", "LNT", "BMRN", "MTCH", "TTD", "TTWO", "DOCU", "ZBRA", "BKR", "QRVO", "SWKS", "FOXA", "FOX"]

class IBKRFinanceOptions:
    def __init__(self, ticker):
        """Initialize with the stock ticker"""
        self.ticker = ticker
        self.contract = Stock(ticker, 'SMART', 'USD')
        ib.qualifyContracts(self.contract)
    
    def get_option_expirations(self):
        """Retrieve available expiration dates for the options."""
        try:
            chains = ib.reqSecDefOptParams(self.ticker, '', self.contract.secType, self.contract.conId)
            if not chains:
                raise ValueError("No option chain data available.")
            expirations = list(set(chains[0].expirations))
            return sorted(expirations)
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
            valid_expirations = [date for date in expirations if datetime.strptime(date, "%Y%m%d") <= max_date]
            
            if not valid_expirations:
                print("No options available within the next 45 days.")
                return None
            
            option_data = {}
            for expiry in valid_expirations:
                try:
                    chains = ib.reqSecDefOptParams(self.ticker, '', 'OPT', self.contract.conId)
                    strikes = sorted(chains[0].strikes)
                    
                    if not strikes:
                        print(f"No valid strikes found for {expiry}.")
                        continue
                    
                    calls = []
                    puts = []
                    for strike in strikes:
                        for right in ['C', 'P']:
                            option_contract = Option(self.ticker, expiry, strike, right, 'SMART', 'USD')
                            ib.qualifyContracts(option_contract)
                            market_data = ib.reqMktData(option_contract, '', False, False)
                            
                            data = {
                                'contractSymbol': option_contract.localSymbol,
                                'lastPrice': market_data.last,
                                'bid': market_data.bid,
                                'ask': market_data.ask,
                                'volume': market_data.volume,
                                'openInterest': market_data.openInterest,
                                'impliedVolatility': market_data.impliedVol,
                                'delta': market_data.delta,
                                'theta': market_data.theta,
                                'gamma': market_data.gamma,
                                'rho': market_data.rho,
                                'ticker': self.ticker
                            }
                            
                            if right == 'C':
                                calls.append(data)
                            else:
                                puts.append(data)
                    
                    df_calls = pd.DataFrame(calls).fillna(0)
                    df_puts = pd.DataFrame(puts).fillna(0)
                    
                    option_data[expiry] = {"calls": df_calls, "puts": df_puts}
                except Exception as e:
                    print(f"Error retrieving option chain for {expiry}: {e}")
            
            return option_data
        except Exception as e:
            print(f"Error processing option chains: {e}")
            return None

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
    
    finance = IBKRFinanceOptions(choice.upper())
    options = finance.get_near_expiry_options()
    
    if options:
        save_to_csv(options, choice.upper())
    else:
        print("No options retrieved.")

if __name__ == "__main__":
    main()
