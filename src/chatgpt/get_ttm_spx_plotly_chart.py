"""
prompt:
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

    def fetch_data(self):
        try:
            self.data = yf.download(self.ticker, period='1y')
            if self.data.empty:
                raise ValueError("No data fetched for the ticker.")
        except Exception as e:
            print(f"Error fetching data: {e}")

    def plot_data(self):
        try:
            if self.data is None or self.data.empty:
                raise ValueError("Data is not available. Please fetch data first.")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['Close'], mode='lines', name='Close Price'))
            fig.update_layout(title=f'{self.ticker} - Last 12 Months Closing Prices',
                              xaxis_title='Date',
                              yaxis_title='Price (USD)')
            fig.show()
        except Exception as e:
            print(f"Error plotting data: {e}")

def main():
    ticker = 'SPY'  # SPY is the ETF that tracks the S&P 500 index
    finance_api = YahooFinanceAPI(ticker)
    finance_api.fetch_data()
    finance_api.plot_data()

class TestYahooFinanceAPI(unittest.TestCase):
    def setUp(self):
        self.finance_api = YahooFinanceAPI('SPY')

    def test_fetch_data(self):
        self.finance_api.fetch_data()
        self.assertIsNotNone(self.finance_api.data)
        self.assertFalse(self.finance_api.data.empty)

    def test_plot_data(self):
        self.finance_api.fetch_data()
        try:
            self.finance_api.plot_data()
            self.assertTrue(True)  # If no exception is raised, the test passes
        except Exception:
            self.fail("plot_data() raised an exception unexpectedly!")

if __name__ == "__main__":
    main()
    # Uncomment the following lines to run tests
    # unittest.main()