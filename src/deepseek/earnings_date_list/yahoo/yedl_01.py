import yfinance as yf
import pandas as pd

# List of NASDAQ stock tickers
nasdaq_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'FB', 'NVDA', 'PYPL', 'INTC', 'CMCSA']

def get_earnings_dates(ticker):
    stock = yf.Ticker(ticker)
    earnings_dates = stock.earnings_dates
    if earnings_dates is not None and not earnings_dates.empty:
        return earnings_dates
    else:
        return None

def main():
    earnings_data = []
    for ticker in nasdaq_tickers:
        earnings_dates = get_earnings_dates(ticker)
        if earnings_dates is not None:
            for index, row in earnings_dates.iterrows():
                earnings_data.append({
                    'Ticker': ticker,
                    'Earnings Date': index.strftime('%Y-%m-%d'),
                    'EPS Estimate': row['EPS Estimate'],
                    'Reported EPS': row['Reported EPS'],
                    'Surprise(%)': row['Surprise(%)']
                })

    # Convert the list to a DataFrame
    earnings_df = pd.DataFrame(earnings_data)

    # Sort by Earnings Date
    earnings_df = earnings_df.sort_values(by='Earnings Date')

    # Print the DataFrame
    print(earnings_df)

    # Save to CSV (optional)
    earnings_df.to_csv('nasdaq_earnings_dates.csv', index=False)

if __name__ == "__main__":
    main()