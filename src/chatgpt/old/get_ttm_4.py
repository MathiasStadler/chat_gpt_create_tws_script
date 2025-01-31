import sys
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import imageio
import os

class StockData:
    def __init__(self, ticker):
        try:
            self.ticker = ticker
            self.data = None
        except Exception as e:
            print(f"Error initializing StockData: {e}")
    
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
            
            temp_images = []
            for i in range(10, len(self.data), 10):  # Every 10th point for animation
                try:
                    fig = go.Figure()
                    fig.add_trace(go.Candlestick(
                        x=self.data.index[:i],
                        open=self.data['Open'][:i],
                        high=self.data['High'][:i],
                        low=self.data['Low'][:i],
                        close=self.data['Close'][:i],
                        name="Candlestick Chart",
                        increasing_line_color='red',
                        decreasing_line_color='red',
                        line={'width': 2}  # Double the line thickness
                    ))
                    
                    temp_filename = f"frame_{i}.png"
                    fig.write_image(temp_filename)
                    temp_images.append(temp_filename)
                except Exception as e:
                    print(f"Error generating frame {i}: {e}")
            
            try:
                with imageio.get_writer(filename, mode='I', duration=0.5) as writer:
                    for img in temp_images:
                        writer.append_data(imageio.imread(img))
                        os.remove(img)
                print(f"GIF saved as {filename}")
            except Exception as e:
                print(f"Error creating GIF: {e}")
        except Exception as e:
            print(f"Error creating plot: {e}")


def main():
    try:
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
    except Exception as e:
        print(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()
