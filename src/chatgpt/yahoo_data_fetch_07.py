# Installation commands
INSTALL_COMMANDS = [
    "pip install yfinance",
    "pip install yahooquery",
    "pip install requests",
    "pip install beautifulsoup4"
]

import yfinance as yf
import requests
from bs4 import BeautifulSoup

class Nasdaq100Stocks:
    def __init__(self):
        self.stocks = []

    def fetch_nasdaq_100(self):
        """Retrieve the latest NASDAQ-100 stock list by scraping the NASDAQ website."""
        try:
            url = "https://www.nasdaq.com/market-activity/stocks/screener"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise ValueError("Failed to fetch data from NASDAQ website.")
            
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            if not table:
                raise ValueError("Could not find the stock table on NASDAQ page.")
            
            self.stocks = [row.find_all("td")[0].text.strip() for row in table.find("tbody").find_all("tr")]
            return self.stocks
        except Exception as e:
            print(f"Error fetching NASDAQ-100 stocks: {e}")
            return []

class StockAnalyzer:
    def __init__(self, symbol):
        self.symbol = symbol

    def fetch_price_volume(self):
        """Fetch stock last price and volume from Yahoo Finance."""
        try:
            stock = yf.Ticker(self.symbol)
            data = stock.history(period="1d")
            if data.empty:
                raise ValueError("No data retrieved. Check the symbol or API availability.")
            last_price = data["Close"].iloc[-1]
            volume = data["Volume"].iloc[-1]
            return last_price, volume
        except Exception as e:
            print(f"Error fetching price and volume for {self.symbol}: {e}")
            return None, None

def main():
    print("Installing required libraries:")
    for cmd in INSTALL_COMMANDS:
        print(f" - {cmd}")
    
    nasdaq = Nasdaq100Stocks()
    nasdaq_100_list = nasdaq.fetch_nasdaq_100()
    if not nasdaq_100_list:
        print("Failed to retrieve NASDAQ-100 stock list.")
        return

    print("NASDAQ-100 Stocks with Last Price and Volume:")
    for stock_symbol in nasdaq_100_list:
        analyzer = StockAnalyzer(stock_symbol)
        price, volume = analyzer.fetch_price_volume()
        if price is not None and volume is not None:
            print(f"{stock_symbol}: Last Price = {price}, Volume = {volume}")

if __name__ == "__main__":
    main()
