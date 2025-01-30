import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import os
import sys
from datetime import datetime, timedelta

class StockData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None

    def download_data(self):
        """Download stock data for the last 12 months."""
        try:
            print(f"Downloading data for {self.ticker}...")
            self.data = yf.download(self.ticker, period="1y")
            if self.data.empty:
                raise ValueError("Downloaded data is empty.")
            print(f"Data for {self.ticker} downloaded successfully.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

    def get_last_12_month_data(self):
        """Return the last 12 months of stock data."""
        try:
            if self.data is None:
                raise ValueError("No data to retrieve.")
            last_12_month_data = self.data
            return last_12_month_data
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

    def plot_data(self):
        """Generate and save a plotly chart as a PNG image."""
        try:
            if self.data is None:
                raise ValueError("No data to plot.")
            
            # Entfernen von Zeilen mit NaN-Werten
            self.data = self.data.dropna()

            # Überprüfen, ob genügend Daten vorhanden sind
            if len(self.data) < 2:
                raise ValueError("Nicht genügend Daten für die Erstellung des Diagramms.")

            fig = make_subplots(rows=1, cols=1)
            fig.add_trace(go.Candlestick(x=self.data.index,
                                         open=self.data['Open'],
                                         high=self.data['High'],
                                         low=self.data['Low'],
                                         close=self.data['Close'], name="Candlestick"))

            # Manuelle Skalierung der Y-Achse
            fig.update_layout(
                title=f'{self.ticker} Stock Data (Last 12 Months)',
                xaxis_title="Date",
                yaxis_title="Price",
                xaxis_rangeslider_visible=False,
                yaxis=dict(
                    rangemode="tozero",  # Y-Achse startet bei 0
                    autorange=True        # Automatische Skalierung aktivieren
                )
            )

            # Plot als PNG speichern
            png_file = f'{self.ticker}_stock_data.png'
            fig.write_image(png_file, format="png")
            print(f"Plot saved as {png_file}")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

def main():
    try:
        # Sicherstellen, dass ein Börsenticker als Argument übergeben wurde
        if len(sys.argv) < 2:
            raise ValueError("Stock ticker argument is missing.")
        
        stock_ticker = sys.argv[1]  # Börsenticker vom Kommandozeilen-Argument abrufen
        stock_data = StockData(stock_ticker)

        # Daten herunterladen und ausgeben
        stock_data.download_data()
        last_12_month_data = stock_data.get_last_12_month_data()
        
        if last_12_month_data is not None:
            print(last_12_month_data)

        # Daten plotten und als PNG speichern
        stock_data.plot_data()

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
