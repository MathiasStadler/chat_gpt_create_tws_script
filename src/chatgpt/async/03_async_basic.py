import asyncio
from ib_async import IB
from ibapi.common import MarketDataType

async def gather_open_positions():
    ib = IB()
    try:
        # Find the next free clientId
        clientId = 1
        while True:
            try:
                await ib.connectAsync('127.0.0.1', 7496, clientId=clientId)
                break
            except ConnectionRefusedError:
                clientId += 1
        
        # Fetch all open positions
        positions = ib.positions()
        
        # Print or process the positions
        for pos in positions:
            print(f"Account: {pos.account}, Symbol: {pos.contract.symbol}, "
                  f"Position: {pos.position}, Avg Cost: {pos.avgCost}")
    finally:
        ib.disconnect()
        # Set market data type to delayed
        ib.reqMarketDataType(MarketDataType.DELAYED)
        
        # Fetch market data for each position
        for pos in positions:
            contract = pos.contract
            # Request market data
            ticker = ib.reqMktData(contract, '', False, False)
            await asyncio.sleep(1)  # Allow time for data to be fetched
            
            # Extract buying rate and current rate
            buying_rate = pos.avgCost
            current_rate = ticker.last if ticker.last else ticker.close
            
            print(f"Account: {pos.account}, Symbol: {contract.symbol}, "
              f"Position: {pos.position}, Buying Rate: {buying_rate}, "
              f"Current Rate: {current_rate}")
if __name__ == "__main__":
    util.patchAsyncio()
    asyncio.run(gather_open_positions())