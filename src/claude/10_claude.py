from ib_async import *
from ibapi.common import MarketDataTypeEnum
import asyncio
from datetime import datetime

class IBPositions:
    def __init__(self):
        self.ib = IB()
    
    async def connect(self):
        await self.ib.connectAsync('127.0.0.1', 7496, clientId=13)
    
    async def get_positions(self):
        try:
            positions = await self.ib.reqPositionsAsync()
            
            print("\nOpen Positions:")
            print("=" * 80)
            
            for pos in positions:
                contract = pos.contract
                details = await self.ib.reqContractDetailsAsync(contract)
                executions = await self.ib.reqExecutionsAsync()
                
                matching_trades = [t for t in executions 
                                 if t.execution.acctNumber == pos.account 
                                 and t.contract.conId == contract.conId]
                
                if matching_trades:
                    avg_price = sum(t.execution.price * t.execution.shares 
                                  for t in matching_trades) / pos.position
                    total_commission = sum(t.commissionReport.commission 
                                        for t in matching_trades)
                    earliest_date = min(t.execution.time for t in matching_trades)
                    
                    print(f"\nSymbol: {contract.symbol}")
                    print(f"Position Size: {pos.position}")
                    print(f"Average Buy Price: ${avg_price:.2f}")
                    print(f"Total Commission: ${total_commission:.2f}")
                    print(f"Initial Position Date: {earliest_date}")
                    print("-" * 80)
                
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            self.ib.disconnect()  # Using regular disconnect instead of async

async def main():
    ib_positions = IBPositions()
    await ib_positions.connect()
    await ib_positions.get_positions()

if __name__ == "__main__":
    asyncio.run(main())