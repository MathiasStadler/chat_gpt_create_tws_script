#!/usr/bin/env python3

import asyncio
import datetime
from ib_insync import IB, util, Contract
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
        portfolio = ib.portfolio()  # Get current portfolio
        
        if portfolio:
            print("\n=== Open Positions ===")
            print(f"{'Symbol':<10} {'SecType':<8} {'Exchange':<10} {'Position':<10} {'Market Price':<15} {'Market Value':<15} {'Avg Price':<15}")
            print("-" * 85)
            
            for position in portfolio:
                symbol = position.contract.symbol
                secType = position.contract.secType
                exchange = position.contract.exchange
                pos_size = position.position
                # Fix: use avgPrice instead of avgCost
                avg_price = position.avgCost
                market_price = position.marketPrice
                market_value = position.marketValue
                
                print(f"{symbol:<10} {secType:<8} {exchange:<10} {pos_size:<10} {market_price:<15.2f} {market_value:<15.2f} {avg_price:<15.2f}")
        else:
            print("\nNo open positions found")
            
        # Alternative approach using positions
        positions = await ib.reqPositionsAsync()
        
        if positions:
            print("\n=== Open Positions (Alternative Method) ===")
            print(f"{'Symbol':<10} {'SecType':<8} {'Exchange':<10} {'Position':<10} {'Avg Price':<15}")
            print("-" * 60)
            
            for pos in positions:
                symbol = pos.contract.symbol
                secType = pos.contract.secType
                exchange = pos.contract.exchange
                pos_size = pos.position
                # Fix: use pos.avgPrice instead of pos.avgCost
                avg_price = pos.avgPrice
                
                print(f"{symbol:<10} {secType:<8} {exchange:<10} {pos_size:<10} {avg_price:<15.2f}")
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
    util.patchAsyncio()
    asyncio.run(main())