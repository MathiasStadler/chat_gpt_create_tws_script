# Python script to connect to TWS using ib-insync
# Python version: 3.x (latest stable version as of January 2025)

# Install necessary packages
# You can run the following command in your terminal or command prompt:
# pip install ib-insync

from ib_insync import *

# Connect to TWS
ip_address = '127.0.0.1'
port = 7496
client_id = 2  # You can choose any client ID

# Create an IB instance
ib = IB()

# Connect to TWS
ib.connect(ip_address, port, clientId=client_id)

# Check if connected
if ib.isConnected():
    print("Successfully connected to TWS!")
else:
    print("Disconnect to connect to TWS.")

# Remember to disconnect when done
ib.disconnect()

# Check if connected
if ib.isConnected():
    print("Successfully connected to TWS!")
else:
    print("Disconnect to connect to TWS.")
