"""
    1. OOP based
    2. with try and error handling for each method
    3. with main function
    4. without  any test case
    5. use the latest stable Python Library
    6. use the Yahoo Finance API 
    7. use the Python Library Plotly Express
    8. Put as command how to install all necessary library
    9. adapt the y axis on the value, leave open 10% and under 10% space
    10. save download data inside a csv file with name of stock
    11. don't overwrite any data files. Check first whether the file exists and if it exists, create a new one
    12. get the data for the last 24 Month
    13. print a chart last  12 month of the stock from first argument.  Use for this the library plotly
    14  add the Simple Moving average  200 in red, Simple Moving average  60 in yellow and the Simple Moving average green
    15. add the indicator Bollinger Bands and make the space between the bands in high blue
    16. gathering the stock ticker from first argument of script call
"""


import sys
import os
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None
        self.file_name = f"{ticker}_stock_data.csv"

    def fetch_data(self):
        """Fetch stock data for the last 24 months."""
        try:
            end_date = datetime.today()
            start_date = end_date - timedelta(days=24*30)
            self.data = yf.download(self.ticker, start=start_date, end=end_date)
            if self.data.empty:
                raise ValueError("No data found for the given ticker.")
        except Exception as e:
            print(f"Error fetching data: {e}")

    def save_data(self):
        """Save data to a CSV file if it doesn't already exist."""
        try:
            if os.path.exists(self.file_name):
                base, ext = os.path.splitext(self.file_name)
                counter = 1
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                self.file_name = f"{base}_{counter}{ext}"
            self.data.to_csv(self.file_name)
            print(f"Data saved to {self.file_name}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def calculate_indicators(self):
        """Calculate SMA and Bollinger Bands."""
        try:
            self.data['SMA_200'] = self.data['Close'].rolling(window=200).mean()
            self.data['SMA_60'] = self.data['Close'].rolling(window=60).mean()
            self.data['SMA_20'] = self.data['Close'].rolling(window=20).mean()
            self.data['Std_Dev'] = self.data['Close'].rolling(window=20).std()
            self.data['Upper_Band'] = self.data['SMA_20'] + (2 * self.data['Std_Dev'])
            self.data['Lower_Band'] = self.data['SMA_20'] - (2 * self.data['Std_Dev'])
        except Exception as e:
            print(f"Error calculating indicators: {e}")

    def plot_data(self):
        """Plot the stock data with indicators."""
        try:
            last_12_months = self.data.tail(12*30)  # Approximate last 12 months
            if last_12_months.empty:
                raise ValueError("Insufficient data for plotting.")

            fig = go.Figure()

            # Plot Close Price
            fig.add_trace(go.Scatter(x=last_12_months.index, y=last_12_months['Close'], mode='lines', name='Close Price'))

            # Plot SMAs
            fig.add_trace(go.Scatter(x=last_12_months.index, y=last_12_months['SMA_200'], mode='lines', name='SMA 200', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=last_12_months.index, y=last_12_months['SMA_60'], mode='lines', name='SMA 60', line=dict(color='yellow')))
            fig.add_trace(go.Scatter(x=last_12_months.index, y=last_12_months['SMA_20'], mode='lines', name='SMA 20', line=dict(color='green')))

            # Plot Bollinger Bands
            fig.add_trace(go.Scatter(x=last_12_months.index, y=last_12_months['Upper_Band'], mode='lines', name='Upper Band', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=last_12_months.index, y=last_12_months['Lower_Band'], mode='lines', name='Lower Band', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=last_12_months.index, y=last_12_months['SMA_20'], mode='lines', name='Middle Band', line=dict(color='blue', dash='dash')))

            # Adjust y-axis
            y_min = last_12_months['Close'].min()
            y_max = last_12_months['Close'].max()
            y_range = y_max - y_min
            fig.update_layout(yaxis_range=[y_min - 0.1 * y_range, y_max + 0.1 * y_range])

            # Show plot
            fig.show()
        except Exception as e:
            print(f"Error plotting data: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <stock_ticker>")
        return

    ticker = sys.argv[1]
    analyzer = StockAnalyzer(ticker)

    analyzer.fetch_data()
    if analyzer.data is not None:
        analyzer.save_data()
        analyzer.calculate_indicators()
        analyzer.plot_data()

if __name__ == "__main__":
    main()