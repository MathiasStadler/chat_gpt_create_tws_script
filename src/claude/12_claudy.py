from ib_async import *
from ibapi.common import MarketDataTypeEnum
import asyncio
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IBPositions:
    def __init__(self):
        self.ib = IB()
        self.account = ""  # Will store the account ID
    
    async def connect(self):
        try:
            await self.ib.connectAsync('127.0.0.1', 7496, clientId=1)
            logger.info("Successfully connected to TWS")
            
            # Wait for account info
            account_data = await self.ib.reqAccountUpdatesAsync()
            self.account = account_data.account
            logger.info(f"Account ID: {self.account}")
            
            return True
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False

    async def get_portfolio(self):
        try:
            logger.info("Requesting portfolio...")
            portfolio = await self.ib.reqPortfolioAsync()
            
            if not portfolio:
                logger.warning("No portfolio items found")
                self._print_troubleshooting()
                return
            
            logger.info(f"Found {len(portfolio)} portfolio items")
            await self._process_portfolio(portfolio)
            
        except Exception as e:
            logger.error(f"Error retrieving portfolio: {str(e)}")
        finally:
            logger.info("Disconnecting from TWS")
            self.ib.disconnect()

    async def _process_portfolio(self, portfolio):
        print("\nPortfolio Positions:")
        print("=" * 80)
        
        for item in portfolio:
            try:
                print(f"\nSymbol: {item.contract.symbol}")
                print(f"Position: {item.position}")
                print(f"Market Price: ${item.marketPrice:.2f}")
                print(f"Market Value: ${item.marketValue:.2f}")
                print(f"Average Cost: ${item.averageCost:.2f}")
                print(f"Unrealized P&L: ${item.unrealizedPNL:.2f}")
                print("-" * 80)
                
            except Exception as e:
                logger.error(f"Error processing portfolio item: {str(e)}")

    def _print_troubleshooting(self):
        print("\nTroubleshooting Guide:")
        print("1. Verify TWS Connection:")
        print("   - TWS is running and you're logged in")
        print("   - API settings are enabled (Configure -> API -> Settings)")
        print("   - 'Read-Only API' is disabled")
        print("\n2. Check Account Status:")
        print("   - You have active positions in your account")
        print("   - Market data subscriptions are active")
        print("\n3. Try These Steps:")
        print("   - Restart TWS")
        print("   - Wait 1-2 minutes after TWS startup")
        print("   - Check TWS API settings")
        print("   - Verify account permissions")

async def main():
    ib_positions = IBPositions()
    if await ib_positions.connect():
        await ib_positions.get_portfolio()

if __name__ == "__main__":
    asyncio.run(main())