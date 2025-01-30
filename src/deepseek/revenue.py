# Python Script to Fetch Sales Figures (Revenue) for a Company
# Python Version: 3.11 (latest stable version as of October 2023)

# Install necessary packages using the following commands:
# pip install yfinance pandas

import yfinance as yf
import pandas as pd

# Define the company ticker symbol (e.g., 'AAPL' for Apple)
company_ticker = 'AAPL'  # Change this to the desired company ticker symbol

# Fetch historical financial data for the company
company = yf.Ticker(company_ticker)

# Get the income statement (annual)
income_statement = company.financials

# Extract revenue (sales) data
revenue = income_statement.loc['Total Revenue']

# Convert the revenue data to a pandas DataFrame for better visualization
revenue_df = pd.DataFrame(revenue).reset_index()
revenue_df.columns = ['Year', 'Total Revenue']

# Print the sales figures for the last few years
print(f"Sales Figures (Total Revenue) for {company_ticker}:\n")
print(revenue_df)

# Optional: Save the revenue data to a CSV file
revenue_df.to_csv(f'{company_ticker}_revenue.csv', index=False)
print(f"\nRevenue data saved to '{company_ticker}_revenue.csv'.")