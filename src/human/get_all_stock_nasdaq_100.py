"""FROM HERE
https://stackoverflow.com/questions/68482251/get-list-of-the-components-of-nasdaq-100
"""

import requests
headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
res=requests.get("https://api.nasdaq.com/api/quote/list-type/nasdaq100",headers=headers)
main_data=res.json()['data']['data']['rows']


for i in range(len(main_data)):
    print(main_data[i]['companyName'])