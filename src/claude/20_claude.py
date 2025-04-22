from ib_async import *
from ibapi.common import MarketDataTypeEnum
import asyncio
from datetime import datetime
import logging
import pandas as pd
from tabulate import tabulate
import os
import sys
from contextlib import redirect_stdout

# Configure base directories
base_dir = "claude"
log_dir = f"{base_dir}/logs"
output_file = f"{base_dir}/19_claude_output.txt"

# Create necessary directories
os.makedirs(base_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# Configure logging
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"{log_dir}/tws_positions_{current_time}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IBPositions:
    def __init__(self):
        self.ib = IB()
        self.account = ""
        self.positions_data = []
        self._connected = False

    async def connect(self):
        try:
            if not self._connected:
                await self.ib.connectAsync('127.0.0.1', 7496, clientId=1)
                logger.info("Successfully connected to TWS")
                
                # Wait for connection to stabilize
                await asyncio.sleep(1)
                
                # Get account information
                if not self.ib.wrapper.accounts:
                    logger.error("No accounts available")
                    return False
                    
                self.account = self.ib.wrapper.accounts[0]
                logger.info(f"Using account: {self.account}")
                
                self._connected = True
            return True
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            self._connected = False
            return False

    async def disconnect(self):
        try:
            if self._connected and self.ib.isConnected():
                logger.info("Disconnecting from TWS...")
                await asyncio.sleep(0.5)
                try:
                    self.ib.disconnect()
                except Exception as e:
                    logger.warning(f"Disconnect warning: {str(e)}")
                finally:
                    self._connected = False
        except Exception as e:
            logger.error(f"Error during disconnect: {str(e)}")

    async def get_portfolio(self):
        if not self._connected:
            logger.error("Not connected to TWS")
            return

        try:
            logger.info("Requesting portfolio...")
            portfolio = await self.ib.reqPositionsAsync()
            
            if not portfolio:
                logger.warning("No portfolio items found")
                self._print_troubleshooting()
                return
            
            logger.info(f"Found {len(portfolio)} portfolio items")
            await self._process_portfolio(portfolio)
            self._create_position_table()
            
        except Exception as e:
            logger.error(f"Error retrieving portfolio: {str(e)}")

    async def _process_portfolio(self, portfolio):
        print("\nPortfolio Positions:")
        print("=" * 80)
        
        for item in portfolio:
            try:
                # Get contract details
                contract_details = await self.ib.reqContractDetailsAsync(item.contract)
                if contract_details:
                    contract = contract_details[0].contract
                    
                    # Request market data using the correct method
                    ticker = self.ib.reqMktData(contract)
                    await asyncio.sleep(2)  # Wait for market data
                    
                    executions = await self.ib.reqExecutionsAsync()
                    matching_trades = [t for t in executions 
                                    if t.contract.conId == item.contract.conId]
                
                    # Get position open date
                    open_dates = [t.execution.time for t in matching_trades if t.execution.side == 'BOT']
                    open_date = min(open_dates) if open_dates else "N/A"
                    earliest_date = min(t.execution.time for t in matching_trades) if matching_trades else "N/A"
                    total_commission = sum(t.commissionReport.commission for t in matching_trades) if matching_trades else 0
                
                    position_info = {
                        "Symbol": item.contract.symbol,
                        "Position": item.position,
                        "Market Price": ticker.last if hasattr(ticker, 'last') and ticker.last else 0.0,
                        "Market Value": (ticker.last * item.position) if hasattr(ticker, 'last') and ticker.last else 0.0,
                        "Commission": total_commission,
                        "Entry Date": earliest_date,
                        "Position Open Date": open_date
                    }
                
                    self.positions_data.append(position_info)
                
                    print(f"\nSymbol: {item.contract.symbol}")
                    print(f"Position: {item.position}")
                    print(f"Market Price: ${position_info['Market Price']:.2f}")
                    print(f"Market Value: ${position_info['Market Value']:.2f}")
                    print(f"Commission: ${total_commission:.2f}")
                    print(f"Entry Date: {earliest_date}")
                    print(f"Position Open Date: {open_date}")
                    print("-" * 80)
                    
                    # Cancel market data subscription
                    self.ib.cancelMktData(contract)
                
            except Exception as e:
                logger.error(f"Error processing portfolio item: {str(e)}")
                logger.error(f"For symbol: {item.contract.symbol}")

    def _create_position_table(self):
        if not self.positions_data:
            logger.warning("No data available for table creation")
            return

        df = pd.DataFrame(self.positions_data)
        
        # Save table to file
        table_filename = f"{log_dir}/positions_table_{current_time}.txt"
        with open(table_filename, 'w') as f:
            f.write("\nPositions Table:\n")
            f.write(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        
        # Display table in console
        print("\nPositions Table:")
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
        logger.info(f"Position table saved to {table_filename}")

    def _print_troubleshooting(self):
        logger.warning("No positions found. Troubleshooting required:")
        logger.warning("1. Verify TWS is running and logged in")
        logger.warning("2. Check API settings in TWS")
        logger.warning("3. Verify account has active positions")
        logger.warning("4. Ensure market data subscriptions are active")

async def main():
    # Redirect stdout to file
    with open(output_file, 'w') as f:
        with redirect_stdout(f):
            ib_positions = IBPositions()
            try:
                if await ib_positions.connect():
                    await ib_positions.get_portfolio()
            except Exception as e:
                logger.error(f"Main execution error: {str(e)}")
            finally:
                if ib_positions._connected:
                    await ib_positions.disconnect()

if __name__ == "__main__":
    asyncio.run(main())