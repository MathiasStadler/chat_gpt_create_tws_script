from ib_insync import *

#Importiere die benötigten Bibliotheken
#Verbinde mit der TWS-Anwendung
ib = IB()
ib.connect('127.0.0.1', 7496, clientId=1)
# Hole Kontoinformationen
account_info = ib.accountSummary()
# Zeige die Kontoinformationen an
for item in account_info:
    print(f'{item.tag}: {item.value}')
    # Trenne die Verbindung
ib.disconnect()
