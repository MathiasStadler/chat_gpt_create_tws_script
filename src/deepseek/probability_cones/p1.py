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
    
"""

import os
import yfinance as yf
import plotly.express as px
import pandas as pd

class StockAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock_data = None
        self.option_chain_data = None

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

    def save_option_chain_data_to_csv(self):
        if self.option_chain_data is not None:
            filename = f"{self.ticker}_option_chain.csv"
            if os.path.exists(filename):
                # If file exists, create a new one with a suffix
                counter = 1
                while os.path.exists(f"{self.ticker}_option_chain_{counter}.csv"):
                    counter += 1
                filename = f"{self.ticker}_option_chain_{counter}.csv"
            self.option_chain_data.calls.to_csv(filename)
            print(f"Option chain data saved to {filename}")
        else:
            print("No option chain data to save.")

    def plot_stock_data(self):
        if self.stock_data is not None:
            try:
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

    # Download and save option chain data
    analyzer.download_option_chain_data()
    analyzer.save_option_chain_data_to_csv()

    # Plot stock data
    analyzer.plot_stock_data()


if __name__ == "__main__":
    main()