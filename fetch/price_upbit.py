"""
Author: yodacatbot@gmail.com
Descriptions:
References:
   - https://steemit.com/kr/@tradingideas/upbit-1
"""

# Python modules
import json
import time
import requests

# Fake User-Agent header;
# Ref: https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Coin name
coinName = "BTC"
# Date (UTC)
dateutc = "2018-03-06"
# Time (UTC)
timeutc = "15:10:00"

# Fetch price from the following url (Upbit temporal API)
url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/10?code=CRIX.UPBIT.USDT-"\
      + coinName\
      + "&count=1&to="\
      + dateutc\
      + "%20"\
      + timeutc

# Try fetching
try:
    fetch = requests.get(url, headers=headers)

except requests.exceptions.HTTPError as err:
    print (err)
    exit(1)

# JSON structure
data = fetch.json()
code = data[0]['code']
print(code)

# Show fetched info.
for i in range(len(data)):
    date = data[i]['candleDateTime']
    onlyDate = date.split('T')
    print(onlyDate[0],
          date,
          "%d"%data[i]['timestamp'],
          "%d"%data[i]['openingPrice'],
          "%d"%data[i]['highPrice'],
          "%d"%data[i]['lowPrice'],
          "%d"%data[i]['tradePrice'],
          "%d"%data[i]['candleAccTradeVolume'],
          "%d"%data[i]['candleAccTradePrice']
          )
