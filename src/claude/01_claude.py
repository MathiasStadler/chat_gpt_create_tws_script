#!/usr/bin/env python3

# crete form here
# https://claude.ai/chat/350a76ff-14e9-49d8-b8f9-4f3329a55a87

# Create a script for the TWS with the following characteristics 
# 1. use programming language Python in the latest stable version
# 2. use the Packages ib-async# 
# 3. use for connect the Application TWS the IP-Address 127.0.0.1  and PORT 7496 
# 4. create a list of all necessary pip3 command for install all necessary packages
# 5. get all Account information from account
# 6. add follow line to script => from ibapi.common import  MarketDataTypeEnum
# 7. create a list all open position inside this account

import asyncio
import datetime
from ib_insync import IB, util
from ibapi.common import MarketDataTypeEnum

async def main():
    # Connect to TWS
    ib = IB()
    try:
        await ib.connectAsync('127.0.0.1', 7496, clientId=1)
        print(f"Connected to TWS at {datetime.datetime.now()}")
        
        # Get account information
        account_summary = await ib.accountSummaryAsync()
        print("\n=== Account Information ===")
        for summary in account_summary:
            print(f"{summary.tag}: {summary.value} {summary.currency}")
        
        # Get portfolio (open positions)
        portfolio = await ib.portfolioAsync()
        
        if portfolio:
            print("\n=== Open Positions ===")
            print(f"{'Symbol':<10} {'Position':<10} {'Avg Cost':<15} {'Market Price':<15} {'Market Value':<15} {'PnL':<10}")
            print("-" * 75)
            
            for position in portfolio:
                symbol = position.contract.symbol
                pos_size = position.position
                avg_cost = position.avgCost
                market_price = position.marketPrice
                market_value = position.marketValue
                unrealized_pnl = position.unrealizedPNL
                
                print(f"{symbol:<10} {pos_size:<10} {avg_cost:<15.2f} {market_price:<15.2f} {market_value:<15.2f} {unrealized_pnl:<10.2f}")
        else:
            print("\nNo open positions found")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Disconnect from TWS
        ib.disconnect()
        print(f"\nDisconnected from TWS at {datetime.datetime.now()}")

if __name__ == "__main__":
    print("Starting TWS account and positions script")
    util.patchAsyncio()
    asyncio.run(main())