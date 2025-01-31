# Importiere die notwendigen Bibliotheken
from ib_insync import *
from ibapi.common import MarketDataTypeEnum

# Verbinde zur TWS
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)

# Hole Kontoinformationen
account_info = ib.accountSummary()
for item in account_info:
    print(f"{item.tag}: {item.value}")

# Trenne die Verbindung
ib.disconnect()