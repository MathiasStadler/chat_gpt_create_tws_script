"""
1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
6.use the library/package request 
6.fetch the data from the URL https://api.nasdaq.com/api/quote/list-type/nasdaq100
7.use the header => "{"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"} "
8.print all stocks with the ticker symbol, last price and the volume
"""

# Installation commands
INSTALL_COMMANDS = [
    "pip install requests"
]

import requests

class Nasdaq100Stocks:
    def __init__(self):
        self.stocks = []

    def fetch_nasdaq_100(self):
        """Retrieve the latest NASDAQ-100 stock list from the NASDAQ API."""
        try:
            url = "https://api.nasdaq.com/api/quote/list-type/nasdaq100"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                raise ValueError("Failed to fetch data from NASDAQ API.")
            
            data = response.json()
            if "data" not in data or "data" not in data["data"]:
                raise ValueError("Invalid response structure from API.")
            
            self.stocks = data["data"]["data"]
            return self.stocks
        except Exception as e:
            print(f"Error fetching NASDAQ-100 stocks: {e}")
            return []

class StockAnalyzer:
    def __init__(self, stock_data):
        self.symbol = stock_data.get("symbol", "N/A")
        self.last_price = stock_data.get("lastsale", "N/A")
        self.volume = stock_data.get("volume", "N/A")

    def display_info(self):
        """Print stock ticker symbol, last price, and volume."""
        try:
            print(f"{self.symbol}: Last Price = {self.last_price}, Volume = {self.volume}")
        except Exception as e:
            print(f"Error displaying stock data: {e}")

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
    for stock_data in nasdaq_100_list:
        analyzer = StockAnalyzer(stock_data)
        analyzer.display_info()

if __name__ == "__main__":
    main()
