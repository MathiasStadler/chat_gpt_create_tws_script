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
    14. remove the space between the charts
    15. add a interactive cursor about both chart
"""

import os
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

# Install necessary libraries
# Run the following command in your terminal:
# pip install yfinance plotly pandas

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None
        self.csv_filename = self._generate_csv_filename()

    def _generate_csv_filename(self):
        base_filename = f"{self.ticker}.csv"
        if not os.path.exists(base_filename):
            return base_filename
        else:
            counter = 1
            while os.path.exists(f"{self.ticker}_{counter}.csv"):
                counter += 1
            return f"{self.ticker}_{counter}.csv"

    def download_data(self):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=24 * 30)  # Last 24 months
            self.data = yf.download(self.ticker, start=start_date, end=end_date)
            if self.data.empty:
                raise ValueError("No data found for the given ticker.")
            self.data.to_csv(self.csv_filename)
            print(f"Data saved to {self.csv_filename}")
            print(self.data.head())  # Debugging: Print the first few rows of data
        except Exception as e:
            print(f"Error downloading data: {e}")

    def plot_data(self):
        if self.data is None:
            print("No data to plot. Please download data first.")
            return

        try:
            # Create subplots
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02, row_heights=[0.7, 0.3])

            # Main plot (Stock Price)
            fig.add_trace(
                go.Scatter(x=self.data.index, y=self.data['Close'], name="Close Price"),
                row=1, col=1
            )

            # Volume plot
            fig.add_trace(
                go.Bar(x=self.data.index, y=self.data['Volume'], name="Volume"),
                row=2, col=1
            )

            # Update layout
            fig.update_layout(
                title=f"{self.ticker} Stock Price and Volume (Last 24 Months)",
                xaxis_title="Date",
                yaxis_title="Price",
                hovermode="x unified",  # Interactive cursor
                showlegend=False
            )

            # Remove space between charts
            fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))

            # Show plot
            fig.show()
        except Exception as e:
            print(f"Error plotting data: {e}")


def main():
    ticker = input("Enter the stock ticker (e.g., AAPL): ").strip().upper()
    analyzer = StockAnalyzer(ticker)

    # Download data
    analyzer.download_data()

    # Plot data
    analyzer.plot_data()


if __name__ == "__main__":
    main()