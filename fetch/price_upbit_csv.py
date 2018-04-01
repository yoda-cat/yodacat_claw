"""
Author
    yodacatbot@gmail.com

Descriptions

References
    # SQL
        https://wikidocs.net/5327
    # Fake User-agent header
        Ref: https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit
"""

# Python modules
import json
import time
import requests
import arrow
import pandas as pd
import sqlite3 as sq3
import time

# Fake User-Agent header
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Coin name
coinName = "BTC"
date_start = arrow.get('2017-09-01 00:00:00', 'YYYY-MM-DD HH:mm:ss')    # Origin: around 2017-09-01
date_end = arrow.get('2017-09-29 00:00:00', 'YYYY-MM-DD HH:mm:ss')
csv_path = 'upbit.csv'

# Variables used for saving fetched data
dateutc = []
timeutc = []
timestamp = []
open = []
high = []
low = []
trade_vol = []
trad_vol_price = []

timestamp_flag = 0
data = []
# Generate time elements
for r in arrow.Arrow.span_range('minute', date_start, date_end):
    bf = str(r[0])
    get_dateutc = bf[0:10]
    get_timeutc = bf[11:19]

    # Fetch price from the following url (Upbit temporal API)
    url = "https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/10?code=CRIX.UPBIT.USDT-"\
          + coinName\
          + "&count=1&to="\
          + get_dateutc\
          + "%20"\
          + get_timeutc

    # Try fetching
    fetch_flag = False
    while fetch_flag == False:
        try:
            fetch = requests.get(url, headers=headers)
            # JSON structure
            data = fetch.json()
            fetch_flag = True
        except:
            print("Fetching error")
            fetch_flag = False

    # Record time series
    if timestamp_flag != data[0]['timestamp']:  # Pass data with same time stamp
        dateutc.append(get_dateutc)
        timeutc.append(get_timeutc)
        timestamp.append(data[0]['timestamp'])
        open.append(round(data[0]['openingPrice'], 2))
        high.append(round(data[0]['highPrice'], 2))
        low.append(round(data[0]['lowPrice'], 2))
        trade_vol.append(round(data[0]['candleAccTradeVolume'], 2))
        trad_vol_price.append(round(data[0]['candleAccTradePrice'], 2))
        print(data)
    else:
        pass
    timestamp_flag = data[0]['timestamp']

# Save valves into .csv
record = pd.DataFrame()
record['dateutc'] = dateutc
record['timeutc'] = timeutc
record['timestamp'] = timestamp
record['open'] = open
record['high'] = high
record['low'] = low
record['tradevol'] = trade_vol
record['tradevolprice'] = trad_vol_price

record.to_csv(csv_path)