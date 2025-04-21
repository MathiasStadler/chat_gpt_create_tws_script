#!/usr/bin/env python3

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
        # The correct way to get portfolio positions is to use ib.positions() method
        # and then access the portfolio attribute
        await ib.reqPositionsAsync()  # Request positions
        portfolio = ib.positions()  # Get positions
        
        if portfolio:
            print("\n=== Open Positions ===")
            print(f"{'Symbol':<10} {'Exchange':<10} {'Position':<10} {'Avg Cost':<15} {'Market Value':<15}")
            print("-" * 70)
            
            for position in portfolio:
                symbol = position.contract.symbol
                exchange = position.contract.exchange
                pos_size = position.position
                avg_cost = position.avgCost
                
                # Get market price for calculating market value
                contract = position.contract
                ticker = await ib.reqMktDataAsync(contract, '', False, False)
                await asyncio.sleep(1)  # Wait for market data to arrive
                
                market_price = ticker.marketPrice()
                market_value = market_price * pos_size if market_price else 0
                
                print(f"{symbol:<10} {exchange:<10} {pos_size:<10} {avg_cost:<15.2f} {market_value:<15.2f}")
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