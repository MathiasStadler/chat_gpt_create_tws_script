"""
ENV: debian 12.8 linux google chrome URL => https://chatgpt.com/ /w register user

prompt:
Create a script for use the Python Library Yahoo Finance API with the following characteristics
    1. OOP based
    2. with try and error handling for each method
    3. with main function
    4. without  any test case
    5. print a chart last  12 month af index SPX use for this the library Plotly. Print the command to install all library
    6. save the downloaded data in a csv file
    7. Use the OHLC chart (for open, high, low and close) is a style of financial chart
    8. Add a vertical and horizontal  slider
    9 don't overwrite any data files. Check first whether the file exists and if it exists, create a new one
"""


import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
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
        """Plot the last 12 months of data using an OHLC chart with Plotly."""
        try:
            if self.data is None or self.data.empty:
                raise ValueError("No data available to plot.")
            
            min_price = self.data['Low'].min()
            max_price = self.data['High'].max()
            price_margin = (max_price - min_price) * 0.1  # 10% space on top and bottom
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=self.data.index,
                open=self.data['Open'],
                high=self.data['High'],
                low=self.data['Low'],
                close=self.data['Close'],
                name=self.ticker
            ))
            
            fig.update_layout(
                title=f"{self.ticker} - Last 12 Months OHLC Chart", 
                xaxis_title="Date", 
                yaxis_title="Price",
                yaxis_range=[min_price - price_margin, max_price + price_margin],  # Adapting Y-axis
                xaxis_rangeslider=dict(visible=True)  # Adding horizontal slider only (vertical slider isn't valid)
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

