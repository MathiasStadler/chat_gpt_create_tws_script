# ...existing code...

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
                
                # Get all managed accounts
                accounts = await self.ib.reqManagedAccountsAsync()
                if not accounts:
                    logger.error("No accounts found")
                    return False
                    
                self.account = accounts[0]
                logger.info(f"Using account: {self.account}")
                
                # Request account updates with the account ID
                await self.ib.reqAccountUpdatesAsync(account=self.account)
                
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
                await asyncio.sleep(0.5)  # Reduced wait time
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
            portfolio = await self.ib.reqPortfolioAsync()
            
            if not portfolio:
                logger.warning("No portfolio items found")
                self._print_troubleshooting()
                return
            
            logger.info(f"Found {len(portfolio)} portfolio items")
            await self._process_portfolio(portfolio)
            self._create_position_table()
            
        except Exception as e:
            logger.error(f"Error retrieving portfolio: {str(e)}")

async def main():
    ib_positions = IBPositions()
    try:
        if await ib_positions.connect():
            await ib_positions.get_portfolio()
    except Exception as e:
        logger.error(f"Main execution error: {str(e)}")
    finally:
        if ib_positions._connected:
            await ib_positions.disconnect()

# ...existing code...