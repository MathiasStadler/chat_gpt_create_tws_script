"""
ENV: debian 12.8 linux google chrome URL => https://chatgpt.com/ /w register user

prompt:
Create a script with the following characteristics
    1. OOP based
    2. with try and error handling for each method
    3. with main function
    4. without  any test case
    5. use the latest stable Python Library
    6. use the Yahoo Finance API 
    7. use the Python Library Plotly Express
    8. Put as command how to install all necessary library
    9. adapt the y axis on the value, leave open 10% and under 10% space
    10. don't overwrite any data files. Check first whether the file exists and if it exists, create a new one
    11. print a chart last  12 month of the stock from first argument.  Use for this the library plotly. 
"""

import yfinance as yf
import plotly.express as px
import pandas as pd
import sys
import os

class YahooFinanceAPI:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.data = None

    def fetch_data(self, period="1y", interval="1d"):
        """Fetch historical data for the given ticker."""
        try:
            stock = yf.Ticker(self.ticker)
            self.data = stock.history(period=period, interval=interval)
            if self.data.empty:
                raise ValueError("No data found for the given ticker.")
            print(f"Successfully fetched data for {self.ticker}")
        except Exception as e:
            print(f"Error fetching data: {e}")
            sys.exit(1)

    def save_to_csv(self, filename="stock_data.csv"):
        """Save the fetched data to a CSV file without overwriting existing files."""
        try:
            if self.data is None or self.data.empty:
                raise ValueError("No data available to save.")
            
            base_filename, extension = os.path.splitext(filename)
            counter = 1
            new_filename = filename
            while os.path.exists(new_filename):
                new_filename = f"{base_filename}_{counter}{extension}"
                counter += 1
            
            self.data.to_csv(new_filename)
            print(f"Data saved to {new_filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
            sys.exit(1)

    def plot_chart(self):
        """Plot the last 12 months of data using an OHLC chart with Plotly Express."""
        try:
            if self.data is None or self.data.empty:
                raise ValueError("No data available to plot.")
            
            min_price = self.data['Low'].min()
            max_price = self.data['High'].max()
            price_margin = (max_price - min_price) * 0.1  # 10% space on top and bottom
            
            fig = px.line(self.data, x=self.data.index, y=['Open', 'High', 'Low', 'Close'], title=f"{self.ticker} - Last 12 Months OHLC Chart")
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price",
                yaxis_range=[min_price - price_margin, max_price + price_margin],  # Adapting Y-axis
                xaxis_rangeslider=dict(visible=True),  # Adding vertical slider
                yaxis_rangeslider=dict(visible=True)   # Adding horizontal slider
            )
            fig.show()
        except Exception as e:
            print(f"Error plotting chart: {e}")
            sys.exit(1)

def main():
    print("Installing required libraries:")
    print("pip install yfinance plotly pandas")
    
    if len(sys.argv) > 1:
        ticker = sys.argv[1]
    else:
        ticker = "^SPX"  # Default ticker if none is provided
    
    yahoo_api = YahooFinanceAPI(ticker)
    yahoo_api.fetch_data()
    yahoo_api.save_to_csv()
    yahoo_api.plot_chart()

if __name__ == "__main__":
    main()


