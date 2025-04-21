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
12. remove the space between the charts
13. use the python library/packages "plotly.graph_objects" and "plotly.subplots"
"""


import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import os

class StockVisualizer:
    def __init__(self, tickers):
        self.tickers = tickers
        self.start_date = datetime.today() - timedelta(days=24*30)  # Last 24 months
        self.end_date = datetime.today()
    
    def fetch_data(self):
        try:
            df = yf.download(self.tickers, start=self.start_date, end=self.end_date, group_by='ticker')
            return df
        except Exception as e:
            print(f"Error in fetching data: {e}")
            return None
    
    def save_data_to_csv(self, df):
        try:
            for ticker in self.tickers:
                file_name = f"{ticker}_data.csv"
                if not os.path.exists(file_name):  # Check if file exists
                    df[ticker].to_csv(file_name)
                else:
                    i = 1
                    while os.path.exists(f"{ticker}_data_{i}.csv"):  # Create new file name if exists
                        i += 1
                    df[ticker].to_csv(f"{ticker}_data_{i}.csv")
        except Exception as e:
            print(f"Error in saving data to CSV: {e}")
    
    def plot_data(self, df):
        try:
            fig = make_subplots(rows=2, cols=1, vertical_spacing=0.05, shared_xaxes=True,
                                subplot_titles=('AAPL Price over time', 'MSFT Price over time'))

            # AAPL Data
            fig.add_trace(go.Scatter(x=df[('AAPL', 'Close')].index,
                                     y=df[('AAPL', 'Close')], line_color='green', marker_color='green',
                                     mode='lines+markers', name="AAPL", stackgroup='one'),
                          row=1, col=1, secondary_y=False)

            # MSFT Data
            fig.add_trace(go.Scatter(x=df[('MSFT', 'Close')].index,
                                     y=df[('MSFT', 'Close')], line_color='blue', mode='lines+markers',
                                     name="MSFT", stackgroup='one'),
                          row=2, col=1, secondary_y=False)

            # Add horizontal lines for AAPL at $125 and MSFT at $150
            fig.add_trace(go.Scatter(x=df[('AAPL', 'Close')].index,
                                     y=[125] * len(df[('AAPL', 'Close')].index), mode='lines',
                                     line_width=3, line_color='black', line_dash='dash', name="AAPL $125"),
                          row=1, col=1, secondary_y=False)

            fig.add_trace(go.Scatter(x=df[('MSFT', 'Close')].index,
                                     y=[150] * len(df[('MSFT', 'Close')].index), mode='lines',
                                     line_width=3, line_color='black', line_dash='dash', name="MSFT $150"),
                          row=2, col=1, secondary_y=False)

            # Update layout
            fig.update_yaxes(tickprefix='$')
            fig.update_xaxes(type='date', range=[df[('AAPL', 'Close')].index.min(), df[('AAPL', 'Close')].index.max()])
            fig.update_layout(hovermode="x unified", dragmode='pan', 
                              xaxis=dict(showspikes=True, spikecolor="black", spikethickness=1),
                              yaxis=dict(showspikes=True, spikecolor="black", spikethickness=1))

            fig.show()
        except Exception as e:
            print(f"Error in plotting data: {e}")

def main():
    # Command to install necessary libraries
    print("Use the following command to install the necessary libraries:")
    print("pip install plotly yfinance pandas")

    # Create the StockVisualizer instance with tickers
    tickers = ['AAPL', 'MSFT']
    visualizer = StockVisualizer(tickers)

    # Fetch stock data
    df = visualizer.fetch_data()
    if df is not None:
        # Save data to CSV
        visualizer.save_data_to_csv(df)
        
        # Plot the data
        visualizer.plot_data(df)
    else:
        print("Failed to fetch data. Exiting...")

if __name__ == "__main__":
    main()
