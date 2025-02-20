"""
1.OOP based
2.with try and error handling for each method
3.with main function
4.without  any test case
5.use the latest stable Python Library
7.use the TWS IBKR  insync API 
8 Create a list on start of the script with command how to install all necessary library
9. use the market data
10. write the result of the script inside a csv file
11. get all next upcoming earnings date with quote
12. please use the paper account on localhost 127.0.0.1 with port 7496 and session id 33)
13, please use market_data_type = MarketDataTypeEnum.DELAYED
14. set market data type to delayed - ib.reqMarketDataType(market_data_type)
15. please add to the imports => from ibapi.common import TickerId, SetOfFloat, SetOfString, MarketDataTypeEnum
"""


# https://www.google.com/search?client=firefox-b-e&channel=entpr&q=ibkr+api+get+earnings+data