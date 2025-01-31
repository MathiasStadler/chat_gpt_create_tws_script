"""
ENV: debian 12.8 linux google chrome URL => https://chatgpt.com/ /w register user

prompt:
Create a script with the following characteristics
    1. OOP based
    2. with try and error handling for each method
    3. with main function
    4. without  any test case
    5. use the latest stable Python Library
    6. use the Yahoo Finance API 
    7. use the Python Library Plotly Express
    8. Put as command how to install all necessary library
    9. adapt the y axis on the value, leave open 10% and under 10% space
    10. don't overwrite any data files. Check first whether the file exists and if it exists, create a new one
    11. get the data for the last 24 Month
    12. print a chart last  12 month of the stock from first argument.  Use for this the library plotly
    13  add the Simple Moving average  200 in red, Simple Moving average  60 in yellow and the Simple Moving average green
    14. Add the indicator Bollinger Bands and make the space between the bands in high blue
    15. 

"""

import yfinance as yf
import plotly.graph_objects as go
import os
import pandas as pd

class StockAnalyzer:
    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.data = None
    
    def fetch_data(self):
        """Fetch stock data for the last 24 months"""
        try:
            self.data = yf.download(self.ticker_symbol, period="2y", interval="1d")
        except Exception as e:
            print(f"Error fetching data for {self.ticker_symbol}: {e}")
            self.data = None
    
    def calculate_sma(self, window=20):
        """Calculate Simple Moving Average (SMA)"""
        try:
            self.data['SMA'] = self.data['Close'].rolling(window=window).mean()
        except Exception as e:
            print(f"Error calculating SMA: {e}")
    
    def calculate_bollinger_bands(self, window=20):
        """Calculate Bollinger Bands"""
        try:
            # Calculate the rolling mean and rolling standard deviation
            self.data['SMA_BB'] = self.data['Close'].rolling(window=window).mean()
            rolling_std = self.data['Close'].rolling(window=window).std()
            
            # Calculate upper and lower Bollinger Bands
            self.data['BB_upper'] = self.data['SMA_BB'] + (rolling_std * 2)
            self.data['BB_lower'] = self.data['SMA_BB'] - (rolling_std * 2)
        except Exception as e:
            print(f"Error calculating Bollinger Bands: {e}")
    
    def plot_data(self):
        """Plot the stock data along with SMA and Bollinger Bands"""
        try:
            if self.data is None:
                print("No data to plot.")
                return
            
            # Plot the Close price and the moving averages
            fig = go.Figure()

            # Add Close price
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['Close'], mode='lines', name='Close', line=dict(color='blue')))
            
            # Add 200 SMA (red)
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['SMA'].rolling(window=200).mean(), mode='lines', name='SMA 200', line=dict(color='red')))
            
            # Add 60 SMA (yellow)
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['SMA'].rolling(window=60).mean(), mode='lines', name='SMA 60', line=dict(color='yellow')))
            
            # Add 20 SMA (green)
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['SMA'].rolling(window=20).mean(), mode='lines', name='SMA 20', line=dict(color='green')))
            
            # Add Bollinger Bands (upper and lower)
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['BB_upper'], mode='lines', name='BB Upper', line=dict(color='blue', dash='dash')))
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['BB_lower'], mode='lines', name='BB Lower', line=dict(color='blue', dash='dash')))
            
            # Adjust the Y-axis to have an open space of 10% above and below the value range
            y_min = self.data['Close'].min() - 0.1 * self.data['Close'].min()
            y_max = self.data['Close'].max() + 0.1 * self.data['Close'].max()
            fig.update_layout(
                yaxis=dict(range=[y_min, y_max]),
                title=f"{self.ticker_symbol} Stock Data with SMAs and Bollinger Bands",
                xaxis_title="Date",
                yaxis_title="Price (USD)"
            )
            
            # Show plot
            fig.show()

        except Exception as e:
            print(f"Error plotting data: {e}")
    
    def save_data(self):
        """Save data to CSV if file doesn't exist, otherwise create a new file."""
        try:
            file_name = f"{self.ticker_symbol}_stock_data.csv"
            if os.path.exists(file_name):
                base_name, ext = os.path.splitext(file_name)
                file_name = f"{base_name}_new{ext}"
            
            self.data.to_csv(file_name)
            print(f"Data saved to {file_name}")
        except Exception as e:
            print(f"Error saving data: {e}")

def main(ticker_symbol):
    """Main function to analyze stock data"""
    try:
        # Initialize StockAnalyzer class
        analyzer = StockAnalyzer(ticker_symbol)
        
        # Fetch stock data for the last 24 months
        analyzer.fetch_data()
        
        if analyzer.data is not None:
            # Calculate Simple Moving Averages (SMA)
            analyzer.calculate_sma(window=200)
            analyzer.calculate_sma(window=60)
            analyzer.calculate_sma(window=20)
            
            # Calculate Bollinger Bands
            analyzer.calculate_bollinger_bands(window=20)
            
            # Plot the data
            analyzer.plot_data()
            
            # Save data to CSV
            analyzer.save_data()

    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    # Example usage: run the script with a stock symbol like "AAPL"
    main("AAPL")