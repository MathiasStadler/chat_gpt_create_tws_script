import asyncio
from ib_async import IB
from ibapi.common import MarketDataTypeEnum

# Define main async function


async def main():
    # Create IB instance and connect to TWS
    ib = IB()
    await ib.connect('127.0.0.1', 7496, clientId=1)

    # Request account summary
    account_summary = await ib.reqAccountSummary()

    print("\n--- Account Information ---\n")
    for row in account_summary.rows:
        print(f"{row.tag}: {row.value} {row.currency} (Account: {row.account})")

    # Request all open positions
    print("\n--- Open Positions ---\n")
    positions = await ib.reqPositions()
    for pos in positions:
        print(f"Account: {pos.account}, Symbol: {pos.contract.symbol}, "
              f"Position: {pos.position}, Avg Cost: {pos.avgCost}")

    # Disconnect from TWS
    await ib.disconnect()

# Run the script
if __name__ == '__main__':
    asyncio.run(main())
