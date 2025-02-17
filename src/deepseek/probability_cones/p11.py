"""
    1. OOP based
    2. with try and error handling for each method
    3. with main function
    4. without  any test case
    5. use the latest stable Python Library
    6. use the latest Yahoo Finance API 
    7. use the Python Library Plotly Express latest version
    8. Put as command how to install all necessary library
    9. adapt the y axis on the value, leave open 10% and under 10% space
    10. save download data inside a csv file with name of stock
    11. don't overwrite any data files. Check first whether the file exists and if it exists, create a new one
    12.  get the option chain data from the stock take by program start use for this yahoo finance
    13. download additional thw greeks of each strike price 
    14. please write option chain with the greeks data in one output file  
"""

import os
import yfinance as yf
import plotly.express as px
import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock_data = None
        self.option_chain_data = None
        self.merged_option_greeks_data = None

    def download_stock_data(self):
        try:
            self.stock_data = yf.download(self.ticker, period="1mo")  # Download 1 month of data
            print(f"Data downloaded for {self.ticker}")
        except Exception as e:
            print(f"Error downloading stock data: {e}")

    def download_option_chain_data(self):
        try:
            stock = yf.Ticker(self.ticker)
            self.option_chain_data = stock.option_chain()
            print(f"Option chain data downloaded for {self.ticker}")
        except Exception as e:
            print(f"Error downloading option chain data: {e}")

    def calculate_greeks(self, row, underlying_price, risk_free_rate=0.01):
        try:
            # Parse expiration date from contractSymbol (e.g., WMT250221P00101000)
            expiration_str = row['contractSymbol'][3:9]  # Extract YYMMDD
            expiration_date = datetime.strptime(expiration_str, "%y%m%d")
            current_date = datetime.now()
            days_to_expiration = (expiration_date - current_date).days
            time_to_expiration = days_to_expiration / 365.0  # Convert to years

            # Black-Scholes formula for Greeks
            S = underlying_price  # Underlying price
            K = row['strike']  # Strike price
            T = time_to_expiration  # Time to expiration
            r = risk_free_rate  # Risk-free rate
            sigma = row['impliedVolatility']  # Implied volatility

            d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            d2 = d1 - sigma * np.sqrt(T)

            # Calculate Greeks
            delta = norm.cdf(d1) if row['Option Type'] == 'Call' else norm.cdf(d1) - 1
            gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
            theta_call = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2))
            theta_put = (-(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2))
            theta = theta_call if row['Option Type'] == 'Call' else theta_put
            theta /= 365  # Convert to daily theta
            vega = S * norm.pdf(d1) * np.sqrt(T) / 100
            rho_call = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
            rho_put = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
            rho = rho_call if row['Option Type'] == 'Call' else rho_put

            return pd.Series({
                'Delta': delta,
                'Gamma': gamma,
                'Theta': theta,
                'Vega': vega,
                'Rho': rho
            })
        except Exception as e:
            print(f"Error calculating Greeks for {row['contractSymbol']}: {e}")
            return pd.Series({
                'Delta': None,
                'Gamma': None,
                'Theta': None,
                'Vega': None,
                'Rho': None
            })

    def merge_option_chain_with_greeks(self):
        try:
            if self.option_chain_data is not None:
                # Extract calls and puts
                calls = self.option_chain_data.calls
                puts = self.option_chain_data.puts
                # Add a column to distinguish between calls and puts
                calls['Option Type'] = 'Call'
                puts['Option Type'] = 'Put'
                # Combine calls and puts into a single DataFrame
                merged_data = pd.concat([calls, puts], axis=0)
                # Get the current stock price
                underlying_price = self.stock_data['Close'].iloc[-1]
                # Calculate Greeks for each option
                greeks = merged_data.apply(
                    self.calculate_greeks,
                    axis=1,
                    underlying_price=underlying_price
                )
                # Merge Greeks with the option chain data
                self.merged_option_greeks_data = pd.concat([merged_data, greeks], axis=1)
                print(f"Option chain and Greeks data merged for {self.ticker}")
            else:
                print("No option chain data available to merge with Greeks.")
        except Exception as e:
            print(f"Error merging option chain with Greeks data: {e}")

    def save_stock_data_to_csv(self):
        if self.stock_data is not None:
            filename = f"{self.ticker}_stock_data.csv"
            if os.path.exists(filename):
                # If file exists, create a new one with a suffix
                counter = 1
                while os.path.exists(f"{self.ticker}_stock_data_{counter}.csv"):
                    counter += 1
                filename = f"{self.ticker}_stock_data_{counter}.csv"
            self.stock_data.to_csv(filename)
            print(f"Stock data saved to {filename}")
        else:
            print("No stock data to save.")

    def save_merged_option_greeks_data_to_csv(self):
        if self.merged_option_greeks_data is not None:
            filename = f"{self.ticker}_option_chain_with_greeks.csv"
            if os.path.exists(filename):
                # If file exists, create a new one with a suffix
                counter = 1
                while os.path.exists(f"{self.ticker}_option_chain_with_greeks_{counter}.csv"):
                    counter += 1
                filename = f"{self.ticker}_option_chain_with_greeks_{counter}.csv"
            # Ensure all columns are properly formatted
            self.merged_option_greeks_data.to_csv(filename, index=False)
            print(f"Merged option chain and Greeks data saved to {filename}")
        else:
            print("No merged option chain and Greeks data to save.")

    def plot_stock_data(self):
        if self.stock_data is not None:
            try:
                # Flatten the multi-index column names
                self.stock_data.columns = self.stock_data.columns.get_level_values(0)
                # Plot the data
                fig = px.line(self.stock_data, y="Close", title=f"{self.ticker} Stock Price")
                # Adjust y-axis with 10% space
                y_max = self.stock_data["Close"].max()
                y_min = self.stock_data["Close"].min()
                fig.update_layout(yaxis_range=[y_min - 0.1 * y_min, y_max + 0.1 * y_max])
                fig.show()
            except Exception as e:
                print(f"Error plotting stock data: {e}")
        else:
            print("No stock data to plot.")


def main():
    ticker = input("Enter the stock ticker (e.g., AAPL): ").strip().upper()
    analyzer = StockAnalyzer(ticker)

    # Download and save stock data
    analyzer.download_stock_data()
    analyzer.save_stock_data_to_csv()

    # Download and merge option chain with Greeks data
    analyzer.download_option_chain_data()
    analyzer.merge_option_chain_with_greeks()
    analyzer.save_merged_option_greeks_data_to_csv()

    # Plot stock data
    analyzer.plot_stock_data()


if __name__ == "__main__":
    main()