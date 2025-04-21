"""
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
    13. add a subplot under the main plot and a volume plot
    14. remove the space between the charts
    15. add a interactive cursor about both chart
"""

import os
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

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
            
            fig = go.Figure()
            
            # Main price chart
            fig.add_trace(go.Candlestick(x=self.data.index,
                                         open=self.data['Open'],
                                         high=self.data['High'],
                                         low=self.data['Low'],
                                         close=self.data['Close'],
                                         name='Price'))
            
            # Volume subplot
            fig.add_trace(go.Bar(x=self.data.index, y=self.data['Volume'], name='Volume', yaxis='y2'))
            
            fig.update_layout(
                title=f"Stock Price and Volume for {self.ticker}",
                xaxis=dict(title='Date', rangeslider=dict(visible=True)),
                yaxis=dict(title='Stock Price'),
                yaxis2=dict(title='Volume', overlaying='y', side='right', showgrid=False),
                hovermode='x unified',  # Interactive cursor
                margin=dict(l=50, r=50, t=50, b=50),
                height=600
            )
            
            fig.show()
        except Exception as e:
            print(f"Error plotting data: {e}")


def main():
    print("To install the necessary libraries, run:")
    print("pip install plotly yfinance pandas")
    
    ticker = input("Enter stock ticker symbol: ")
    stock = StockData(ticker)
    stock.fetch_data()
    stock.save_to_csv()
    stock.plot_data()

if __name__ == "__main__":
    main()
