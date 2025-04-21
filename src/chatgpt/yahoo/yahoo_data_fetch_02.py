"""
1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
7.use the Python Yahoo Finance API 
8 Create a list on start of the script with command how to install all necessary library
9.retrieve all stock of the NASDAQ 100 and create a list

"""

# Installation commands
INSTALL_COMMANDS = [
    "pip install yfinance"
]

import yfinance as yf

class Nasdaq100Stocks:
    def __init__(self):
        self.stocks = []

    def fetch_nasdaq_100(self):
        """Retrieve a predefined list of NASDAQ-100 stocks."""
        try:
            self.stocks = [
                "AAPL", "MSFT", "AMZN", "GOOGL", "GOOG", "FB", "TSLA", "NVDA", "PYPL", "ADBE",
                "NFLX", "INTC", "CMCSA", "PEP", "AVGO", "COST", "CSCO", "TXN", "QCOM", "TMUS",
                "AMGN", "SBUX", "CHTR", "GILD", "MDLZ", "ISRG", "BKNG", "ADP", "VRTX", "INTU",
                "REGN", "LRCX", "ASML", "ATVI", "DASH", "MRNA", "PDD", "JD", "MU", "ZM",
                "ABNB", "BIDU", "ILMN", "SNPS", "ADI", "MELI", "KDP", "DXCM", "MAR", "LULU",
                "EXC", "EA", "XEL", "WDAY", "PANW", "ORLY", "MNST", "IDXX", "ROST", "CTAS",
                "CDNS", "PAYX", "AEP", "KHC", "PCAR", "ALGN", "BIIB", "FTNT", "CSX", "SPLK",
                "VRSK", "CHKP", "FAST", "KLAC", "WBA", "DLTR", "SWKS", "NXPI", "CDW", "CEG",
                "ANSS", "EBAY", "CTSH", "TTWO", "SIRI", "FOXA", "FOX", "VRSN", "NTAP", "SGEN",
                "MTCH", "CPRT", "AZN", "ZS", "ODFL", "TTD", "TEAM", "OKTA", "DDOG", "CRWD"
            ]
            return self.stocks
        except Exception as e:
            print(f"Error fetching NASDAQ-100 stocks: {e}")
            return []

class StockAnalyzer:
    def __init__(self, symbol):
        self.symbol = symbol
        self.data = None

    def fetch_data(self, period="1y", interval="1d"):
        """Fetch stock data from Yahoo Finance."""
        try:
            stock = yf.Ticker(self.symbol)
            self.data = stock.history(period=period, interval=interval)
            if self.data.empty:
                raise ValueError("No data retrieved. Check the symbol or API availability.")
            return self.data
        except Exception as e:
            print(f"Error fetching data for {self.symbol}: {e}")
            return None


def main():
    print("Installing required libraries:")
    for cmd in INSTALL_COMMANDS:
        print(f" - {cmd}")
    
    nasdaq = Nasdaq100Stocks()
    nasdaq_100_list = nasdaq.fetch_nasdaq_100()
    print("NASDAQ-100 Stocks:", nasdaq_100_list)

    if nasdaq_100_list:
        stock_symbol = nasdaq_100_list[0]  # Example: First stock in the list
        analyzer = StockAnalyzer(stock_symbol)
        data = analyzer.fetch_data()
        if data is not None:
            print(data.head())

if __name__ == "__main__":
    main()
