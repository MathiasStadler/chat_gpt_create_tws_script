#!/usr/bin/env python3

# https://claude.ai/chat/350a76ff-14e9-49d8-b8f9-4f3329a55a87

import datetime
import nest_asyncio
from ib_async import IB
from ibapi.common import MarketDataTypeEnum

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

def main():
    # Connect to TWS
    ib = IB()
    try:
        # Connect synchronously
        ib.connect('127.0.0.1', 7496, clientId=1)
        print(f"Connected to TWS at {datetime.datetime.now()}")
        
        # Get account information
        account_summary = ib.accountSummary()
        print("\n=== Account Information ===")
        for summary in account_summary:
            print(f"{summary.tag}: {summary.value} {summary.currency}")
        
        # Get portfolio (open positions)
        portfolio = ib.portfolio()
        
        if portfolio:
            print("\n=== Open Positions ===")
            print(f"{'Symbol':<10} {'SecType':<8} {'Exchange':<10} {'Position':<10} {'Market Price':<15} {'Market Value':<15}")
            print("-" * 70)
            
            for position in portfolio:
                symbol = position.contract.symbol
                secType = position.contract.secType
                exchange = position.contract.exchange
                pos_size = position.position
                
                # Use hasattr to check for attribute existence and print available attributes
                if hasattr(position, "marketPrice"):
                    market_price = position.marketPrice
                else:
                    market_price = 0
                    
                if hasattr(position, "marketValue"):
                    market_value = position.marketValue
                else:
                    market_value = 0
                
                print(f"{symbol:<10} {secType:<8} {exchange:<10} {pos_size:<10} {market_price:<15.2f} {market_value:<15.2f}")
                
            # Debug information - print all available attributes
            if portfolio:
                print("\n=== Debug: Available Attributes ===")
                print(dir(portfolio[0]))
        else:
            print("\nNo open positions found")
            
        # Alternative approach using positions
        positions = ib.positions()
        
        if positions:
            print("\n=== Open Positions (Alternative Method) ===")
            print(f"{'Symbol':<10} {'SecType':<8} {'Exchange':<10} {'Position':<10}")
            print("-" * 40)
            
            for pos in positions:
                symbol = pos.contract.symbol
                secType = pos.contract.secType
                exchange = pos.contract.exchange
                pos_size = pos.position
                
                print(f"{symbol:<10} {secType:<8} {exchange:<10} {pos_size:<10}")
                
            # Debug information - print all available attributes
            if positions:
                print("\n=== Debug: Available Attributes (Alternative Method) ===")
                print(dir(positions[0]))
        else:
            print("\nNo open positions found (alternative method)")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Disconnect from TWS
        ib.disconnect()
        print(f"\nDisconnected from TWS at {datetime.datetime.now()}")

if __name__ == "__main__":
    print("Starting TWS account and positions script")
    main()