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

import requests

class NasdaqDataFetcher:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.data = None

    def fetch_data(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            self.data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")

    def parse_and_print_data(self):
        if self.data:
            try:
                # stocks = self.data.get("data").get("rows")
                
                 
                stocks = self.data.data
                data = self.data.get("data", {})
                rows = self.data.get("data").get("rows")
                print( rows[0])
                #print(stocks.get("data").get("rows"))
                if not stocks:
                    print("No stocks found in the response.")
                    return
                for stock in stocks:
                    ticker = stock.get("symbol", "N/A")
                    last_price = stock.get("lastSalePrice", "N/A")
                    volume = stock.get("volume", "N/A")
                    print(f"Ticker: {ticker}, Last Price: {last_price}, Volume: {volume}")
            except Exception as e:
                print(f"Error parsing data: {e}")
        else:
            print("No data available to parse.")

def main():
    url = "https://api.nasdaq.com/api/quote/list-type/nasdaq100"
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    
    fetcher = NasdaqDataFetcher(url, headers)
    fetcher.fetch_data()
    fetcher.parse_and_print_data()

if __name__ == "__main__":
    main()
