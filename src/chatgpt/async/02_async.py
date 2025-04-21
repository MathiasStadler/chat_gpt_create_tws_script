import asyncio
from ib_async import IB
from ibapi.common import MarketDataTypeEnum

async def run_ib_script():
    ib = IB()
    await ib.connect('127.0.0.1', 7496, clientId=13)

    account_summary = await ib.reqAccountSummary()
    print("\n--- Account Information ---\n")
    for row in account_summary.rows:
        print(f"{row.tag}: {row.value} {row.currency} (Account: {row.account})")

    positions = await ib.reqPositions()
    print("\n--- Open Positions ---\n")
    for pos in positions:
        print(f"Account: {pos.account}, Symbol: {pos.contract.symbol}, "
              f"Position: {pos.position}, Avg Cost: {pos.avgCost}")

    await ib.disconnect()

# Run this in Jupyter cell
await run_ib_script()
