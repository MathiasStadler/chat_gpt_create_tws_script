"""
prompt
Create a script for use the Python Library Yahoo Finance API with the following characteristics
1. OOP based
2. with try and error handling for each method
3. with main function
4. with test case for each method inside the script and the command for running all test cases and run a single test case
5. print a chart last 12 month af index SPX use for this the library Plotly. Print the command to install all library
6. plot the last six month at start screen
"""

import yfinance as yf
import plotly.graph_objects as go
import unittest

class YahooFinanceAPI:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None

    def fetch_data(self, period='1y'):
        try:
            self.data = yf.download(self.ticker, period=period)
            if self.data.empty:
                raise ValueError("No data fetched for the given ticker.")
        except Exception as e:
            print(f"Error fetching data: {e}")

    def plot_data(self, period='1y'):
        try:
            if self.data is None:
                self.fetch_data(period)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['Close'], mode='lines', name=self.ticker))
            fig.update_layout(title=f'{self.ticker} Price Over Last {period}', xaxis_title='Date', yaxis_title='Price')
            fig.show()
        except Exception as e:
            print(f"Error plotting data: {e}")

def main():
    ticker = '^SPX'
    finance_api = YahooFinanceAPI(ticker)
    
    # Plot last 6 months data at start
    finance_api.plot_data(period='6mo')
    
    # Plot last 12 months data
    finance_api.plot_data(period='1y')

if __name__ == "__main__":
    main()

# Test cases
class TestYahooFinanceAPI(unittest.TestCase):
    def setUp(self):
        self.api = YahooFinanceAPI('AAPL')

    def test_fetch_data(self):
        self.api.fetch_data()
        self.assertIsNotNone(self.api.data)
        self.assertFalse(self.api.data.empty)

    def test_plot_data(self):
        self.api.fetch_data()
        try:
            self.api.plot_data()
        except Exception as e:
            self.fail(f"plot_data raised Exception: {e}")

if __name__ == '__main__':
    unittest.main()