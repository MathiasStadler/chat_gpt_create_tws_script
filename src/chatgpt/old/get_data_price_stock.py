"""
prompt
Create a script for use the Python Library Yahoo Finance API with the following characteristics
1. OOP based
2. with try and error handling for each method
3. with main function
4. with test case for each method inside the script and the command for running all test cases and run a single test case
5. add  try und except conditioen each function methode
6. generate no test case 
6. download stock data last 12 month  and print as a list
7. Take the first argument that was specified when the program started at stock ticker
8. create from the download data a plotly chart and save as as png format

"""

import sys
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import imageio
import os

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None
    
    def download_data(self):
        try:
            self.data = yf.download(self.ticker, period="12mo")
            if self.data.empty:
                raise ValueError("No data found for ticker: " + self.ticker)
            return self.data
        except Exception as e:
            print(f"Error downloading data: {e}")
            return None
    
    def get_data_as_list(self):
        try:
            if self.data is None:
                raise ValueError("Data not downloaded yet.")
            return self.data[['Open', 'High', 'Low', 'Close', 'Volume']].values.tolist()
        except Exception as e:
            print(f"Error converting data to list: {e}")
            return []
    
    def plot_and_save(self, filename="stock_chart.gif"):
        try:
            if self.data is None:
                raise ValueError("Data not downloaded yet.")
            
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=self.data.index,
                open=self.data['Open'],
                high=self.data['High'],
                low=self.data['Low'],
                close=self.data['Close'],
                name="Candlestick Chart"
            ))
            
            temp_images = []
            for i in range(1, len(self.data), 10):  # Every 10th point for animation
                temp_filename = f"frame_{i}.png"
                fig.update_traces(x=self.data.index[:i], open=self.data['Open'][:i],
                                  high=self.data['High'][:i], low=self.data['Low'][:i],
                                  close=self.data['Close'][:i])
                fig.write_image(temp_filename)
                temp_images.append(temp_filename)
            
            with imageio.get_writer(filename, mode='I', duration=0.5) as writer:
                for img in temp_images:
                    writer.append_data(imageio.imread(img))
                    os.remove(img)
            
            print(f"GIF saved as {filename}")
        except Exception as e:
            print(f"Error creating plot: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <STOCK_TICKER>")
        return
    
    ticker = sys.argv[1]
    stock = StockData(ticker)
    
    data = stock.download_data()
    if data is not None:
        print("Stock Data as List:")
        print(stock.get_data_as_list())
        stock.plot_and_save()


if __name__ == "__main__":
    main()

# Test cases
import unittest

class TestStockData(unittest.TestCase):
    def setUp(self):
        self.stock = StockData("AAPL")

    def test_download_data(self):
        data = self.stock.download_data()
        self.assertIsNotNone(data)
        self.assertFalse(data.empty)

    def test_get_data_as_list(self):
        self.stock.download_data()
        data_list = self.stock.get_data_as_list()
        self.assertIsInstance(data_list, list)
        self.assertGreater(len(data_list), 0)

    def test_plot_and_save(self):
        self.stock.download_data()
        self.stock.plot_and_save("test.gif")
        self.assertTrue(os.path.exists("test.gif"))
        os.remove("test.gif")

if __name__ == "__main__":
    unittest.main()
