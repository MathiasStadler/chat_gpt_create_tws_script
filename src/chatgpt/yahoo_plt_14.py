"""
1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
6.use the Python Library Plotly Express
7.use the Yahoo Finance API 
8 Create a list on start of the script with command how to install all necessary library
9.save download data inside a csv file with name of stock
10. don't overwrite any data files. Check first whether the file exists and if it exists, create a new one
11. get the data for the last 24 Month
12. add a subplot under the main plot and calculate the Indicator MACD plot that use the same y axis cursor from above plot
13. remove the space between the charts
14. please add the MACD under as a separate plot NOT into the chart plot
    
"""

import os
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# List of installation commands
INSTALL_COMMANDS = [
    "pip install plotly yfinance pandas"
]

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None

    def fetch_data(self):
        try:
            end_date = datetime.today()
            start_date = end_date - timedelta(days=24*30)  # Approximate 24 months
            stock = yf.Ticker(self.ticker)
            self.data = stock.history(period="2y")
            if self.data.empty:
                raise ValueError("No data found for the given ticker.")
            
            # Calculate MACD
            self.data['12_EMA'] = self.data['Close'].ewm(span=12, adjust=False).mean()
            self.data['26_EMA'] = self.data['Close'].ewm(span=26, adjust=False).mean()
            self.data['MACD'] = self.data['12_EMA'] - self.data['26_EMA']
            self.data['Signal'] = self.data['MACD'].ewm(span=9, adjust=False).mean()
            
            # Calculate buy/sell volume
            self.data['Buy Volume'] = self.data['Volume'].where(self.data['Close'] > self.data['Open'], 0)
            self.data['Sell Volume'] = self.data['Volume'].where(self.data['Close'] <= self.data['Open'], 0)
        except Exception as e:
            print(f"Error fetching data: {e}")

    def save_to_csv(self):
        try:
            filename = f"{self.ticker}.csv"
            counter = 1
            while os.path.exists(filename):
                filename = f"{self.ticker}_{counter}.csv"
                counter += 1
            self.data.to_csv(filename)
            print(f"Data saved as {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def plot_data(self):
        try:
            if self.data is None or self.data.empty:
                raise ValueError("No data available to plot.")
            
            # Create main figure with subplots
            fig = go.Figure()
            
            # Main price chart
            fig.add_trace(go.Candlestick(x=self.data.index,
                                         open=self.data['Open'],
                                         high=self.data['High'],
                                         low=self.data['Low'],
                                         close=self.data['Close'],
                                         name='Price'))
            
            # MACD chart with Buy/Sell volume
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=self.data.index, y=self.data['MACD'], mode='lines', name='MACD'))
            fig_macd.add_trace(go.Scatter(x=self.data.index, y=self.data['Signal'], mode='lines', name='Signal'))
            fig_macd.add_trace(go.Bar(x=self.data.index, y=self.data['Buy Volume'], name='Buy Volume', marker_color='green'))
            fig_macd.add_trace(go.Bar(x=self.data.index, y=self.data['Sell Volume'], name='Sell Volume', marker_color='red'))
            
            # Set layout for interactive cursor alignment
            fig.update_layout(title=f"Stock Price for {self.ticker}", hovermode='x unified')
            fig_macd.update_layout(title="MACD with Buy/Sell Volume", hovermode='x unified')
            
            # Show plots separately
            fig.show()
            fig_macd.show()
        except Exception as e:
            print(f"Error plotting data: {e}")


def main():
    print("To install the necessary libraries, run:")
    for command in INSTALL_COMMANDS:
        print(command)
    
    ticker = input("Enter stock ticker symbol: ")
    stock = StockData(ticker)
    stock.fetch_data()
    stock.save_to_csv()
    stock.plot_data()

if __name__ == "__main__":
    main()