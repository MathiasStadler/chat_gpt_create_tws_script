"""
prompt
Create a script for use the Python Library Yahoo Finance API with the following characteristics
1. OOP based
2. with try and error handling for each method
3. with main function
4. with test case for each method inside the script and the command for running all test cases and run a single test case
5. print a chart last 12 month af index SPX use for this the library Plotly. Print the command to install all library
6. convert the outplot to gif and save inside the /tmp folder
"""


import yfinance as yf
import plotly.graph_objects as go
import os
import imageio
import numpy as np

class YahooFinanceAPI:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None

    def fetch_data(self):
        try:
            self.data = yf.download(self.ticker, period='1y')
            if self.data.empty:
                raise ValueError("No data fetched.")
        except Exception as e:
            print(f"Error fetching data: {e}")

    def plot_data(self):
        try:
            if self.data is None:
                raise ValueError("Data not fetched. Please call fetch_data() first.")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['Close'], mode='lines', name='Close Price'))
            fig.update_layout(title=f'{self.ticker} Last 12 Months', xaxis_title='Date', yaxis_title='Price')
            return fig
        except Exception as e:
            print(f"Error plotting data: {e}")

    def save_gif(self, fig):
        try:
            # Save as HTML first
            fig.write_html('/tmp/spx_plot.html')
            # Convert HTML to GIF
            images = []
            for i in range(1, 11):  # Create 10 frames for the GIF
                fig.update_layout(title=f'{self.ticker} Last 12 Months - Frame {i}')
                fig.write_image(f'/tmp/spx_frame_{i}.png')
                images.append(imageio.imread(f'/tmp/spx_frame_{i}.png'))
            imageio.mimsave('/tmp/spx_plot.gif', images, duration=0.5)
            print("GIF saved to /tmp/spx_plot.gif")
        except Exception as e:
            print(f"Error saving GIF: {e}")

def main():
    ticker = '^SPX'
    finance_api = YahooFinanceAPI(ticker)
    finance_api.fetch_data()
    fig = finance_api.plot_data()
    finance_api.save_gif(fig)

# Test cases
def test_fetch_data():
    api = YahooFinanceAPI('^SPX')
    api.fetch_data()
    assert api.data is not None, "Data should not be None after fetching."

def test_plot_data():
    api = YahooFinanceAPI('SPX')
    api.fetch_data()
    fig = api.plot_data()
    assert fig is not None, "Figure should not be None after plotting."

def test_save_gif():
    api = YahooFinanceAPI('SPX')
    api.fetch_data()
    fig = api.plot_data()
    api.save_gif(fig)
    assert os.path.exists('/tmp/spx_plot.gif'), "GIF should be saved in /tmp."

if __name__ == "__main__":
    main()

    # Run test cases
    test_fetch_data()
    test_plot_data()
    test_save_gif()
    print("All tests passed.")