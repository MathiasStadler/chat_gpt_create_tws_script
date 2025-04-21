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
"""


import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import sys

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

    def save_to_csv(self, filename="spx_data.csv"):
        """Save the fetched data to a CSV file."""
        try:
            if self.data is None or self.data.empty:
                raise ValueError("No data available to save.")
            self.data.to_csv(filename)
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data: {e}")
            sys.exit(1)

    def plot_chart(self):
        """Plot the last 12 months of data using an OHLC chart with Plotly."""
        try:
            if self.data is None or self.data.empty:
                raise ValueError("No data available to plot.")
            
            fig = go.Figure()
            fig.add_trace(go.Ohlc(
                x=self.data.index,
                open=self.data['Open'],
                high=self.data['High'],
                low=self.data['Low'],
                close=self.data['Close'],
                name=self.ticker
            ))
            fig.update_layout(title=f"{self.ticker} - Last 12 Months OHLC Chart", 
                              xaxis_title="Date", 
                              yaxis_title="Price")
            fig.show()
        except Exception as e:
            print(f"Error plotting chart: {e}")
            sys.exit(1)

def main():
    print("Installing required libraries:")
    print("pip install yfinance plotly pandas")
    
    ticker = "^SPX"
    yahoo_api = YahooFinanceAPI(ticker)
    yahoo_api.fetch_data()
    yahoo_api.save_to_csv()
    yahoo_api.plot_chart()

if __name__ == "__main__":
    main()
