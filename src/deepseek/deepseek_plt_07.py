"""
    https://chatgpt.com/ /w login 
    Generate a script 
    1. OOP based
    2. with try and error handling for each method
    3. with main function
    4. without  any test case
    5. use the latest stable Python Library
    6. use the Python Library Plotly Express
    6. use the Yahoo Finance API 
    7. Print as command how to install all necessary library
    8. save download data inside a csv file with name of stock
    11. don't overwrite any data files. Check first whether the file exists and if it exists, create a new one
    12. get the data for the last 24 Month
    13 add a subplot under the main plot and a volume plot
    14. generate separate plot for each
"""

import os
import yfinance as yf
import plotly.graph_objects as go
import plotly.offline as pyo
import pandas as pd
from datetime import datetime, timedelta

class StockDataFetcher:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.data = None

    def fetch_data(self):
        try:
            stock = yf.Ticker(self.ticker)
            end_date = datetime.today()
            start_date = end_date - timedelta(days=730)  # Last 24 months
            self.data = stock.history(period='1d', start=start_date, end=end_date)
            if self.data.empty:
                raise ValueError("No data found for the given ticker.")
        except Exception as e:
            print(f"Error fetching stock data: {e}")

    def save_to_csv(self):
        try:
            if self.data is None:
                raise ValueError("No data to save. Fetch data first.")
            
            filename = f"{self.ticker}.csv"
            count = 1
            while os.path.exists(filename):
                filename = f"{self.ticker}_{count}.csv"
                count += 1
            
            self.data.to_csv(filename)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving CSV file: {e}")

    def plot_data(self):
        try:
            if self.data is None:
                raise ValueError("No data to plot. Fetch data first.")
            
            # Plot Close Price
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=self.data.index, y=self.data['Close'], mode='lines', name='Close Price'))
            fig1.update_layout(title=f"Stock Prices for {self.ticker}", xaxis_title="Date", yaxis_title="Close Price")
            pyo.plot(fig1, filename=f"{self.ticker}_price.html")
            
            # Plot Volume as a separate figure
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=self.data.index, y=self.data['Volume'], name='Volume'))
            fig2.update_layout(title=f"Trading Volume for {self.ticker}", xaxis_title="Date", yaxis_title="Volume")
            pyo.plot(fig2, filename=f"{self.ticker}_volume.html")
        except Exception as e:
            print(f"Error generating plot: {e}")

def main():
    print("To install necessary libraries, run:")
    print("pip install yfinance plotly pandas")
    
    ticker = input("Enter stock ticker symbol: ").upper()
    stock_fetcher = StockDataFetcher(ticker)
    stock_fetcher.fetch_data()
    stock_fetcher.save_to_csv()
    stock_fetcher.plot_data()

if __name__ == "__main__":
    main()
