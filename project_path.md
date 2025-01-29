## date today 

```bach
date
Tue Jan 29 04:19:03 PM CET 2025
```


## os- version

```bash
Linux debian 6.1.0-28-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.119-1 (2024-11-22) x86_64 GNU/Linux
```

# installed python version 

```bash
python3 --version
Python 3.11.2
```
# create python venv

[install venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

```bash
python3 -m venv .venv
```

## enter .venv

```bash
source .venv//bin/activate
```

## exit/leave venv

```bash
deactivate
```

# start the TOS local


# install ib_insync

```bash
pip3 install ib_insync
```


## 1. promt for account info

```text
Create a script for the TWS with the following characteristics
1. use programming language Python in the latest stable version
2. use the Packages ib-insync
3. use for connect the Application TWS the IP-Address 127.0.0.1 and PORT 7496
4. create a list of all necessary pip3 command for install all necessary packages
5. get all konto information from account
```

## 2. propt output format as text no html

```text
Create a script for the TWS with the following characteristics
1. create the script as text without any html tags
2. use programming language Python in the latest stable version
3. use the Packages ib-insync
4. use for connect the Application TWS the IP-Address 127.0.0.1 and PORT 7496
5. create a list of all necessary pip3 command for install all necessary packages
6. get all konto information from account
```

## 3 prompt current value of stock TREX

```text
Create a script for the TWS with the following characteristics
1. create the script as text without any html tags
2. use programming language Python in the latest stable version
3. use the Packages ib-insync
4. create a list of command to install all necessary packages
4. use for connect the Application TWS the IP-Address 127.0.0.1 and PORT 7496
```

## 3.1 

Create a script for the TWS with the following characteristics
1. create the script as text without any html tags
2. use programming language Python in the latest stable version and display inside the script the version
3. use the Packages ib-insync
4. create a list of command to install all necessary packages
5. use for connect the Application TWS the IP-Address 127.0.0.1 and PORT 7496

## 3.2 get option chain - in function

Create a script for the TWS with the following characteristics
1. create the script as text without any html tags
2. use programming language Python in the latest stable version and display inside the script the version
3. use the Packages ib-insync
4. create a list of command to install all necessary packages
5. use for connect the Application TWS the IP-Address 127.0.0.1 and PORT 7496
6. print the price from  the stock TREX list on SMART
7. please use MarketDataTypeEnum.DELAYED and add the import statement to script


### 3.3

Create a script for the TWS with the following characteristics
1. create the script as text without any html tags
2. use programming language Python in the latest stable version and display inside the script the version
3. use the Packages ib-insync
4. create a list of command to install all necessary packages
5. use for connect the Application TWS the IP-Address 127.0.0.1 and PORT 7496
6. print the price from  the stock TREX list on SMART
7. please use MarketDataTypeEnum.DELAYED and add the import statement to script
8. please print contract id of contract
9. print the option chain expiration dates of the stock
10. add follow line to script => from ibapi.common import MarketDataTypeEnum
11. please use ib.qualifyContracts for full filled the contract


Create a script for the TWS with the following characteristics
1. create the script as text without any html tags
2. use programming language Python in the latest stable version and display inside the script the version
3. use the Packages ib-insync
4. create a list of command to install all necessary packages
5. use for connect the Application TWS the IP-Address 127.0.0.1 and PORT 7496
6. print the price from  the stock TREX list on SMART
7. please use MarketDataTypeEnum.DELAYED and add the import statement to script
8. please print contract id of contract
9. print the option chain expiration dates of the stock
10. add follow line to script => from ibapi.common import MarketDataTypeEnum
11. please use ib.qualifyContracts for full filled the contract
12. add the option chain too to each expiration date Call and put side