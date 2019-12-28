#!/usr/bin/env python

import requests
from datetime import datetime

ts_start = int(datetime(2019, 7, 31).timestamp())
ts_end = int(datetime.today().timestamp())

coins = ["bitcoin", "bitcoin-cash", "ethereum", "ripple", "litecoin", "filecoin"]
all = {}
for coin in coins:
    print(f"Getting prices for {coin}")
    url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?convert=USD"
    url += f"&slug={coin}"
    url += f"&time_end={ts_end}"
    url += f"&time_start={ts_start}"

    resp = requests.get(url)
    data = resp.json()['data']

    prices = [(x['time_open'][:10], x['quote']['USD']['close']) for x in data['quotes']]
    for ts, price in prices:
        ts = datetime.strptime(ts, "%Y-%m-%d")
        if ts == ts.replace(day=1):
            # First day of month
            datestr = ts.strftime('%Y-%m-%d')
            all.setdefault(datestr, {})
            all[datestr][coin] =  price
            print(f"{ts.strftime('%Y-%m-%d')}	{price}")

#print(all)

rows =  ["date," + ','.join(coins)]
for ts, prices in all.items():
    row = f"{ts},"
    row += ",".join([str(val) for _, val in prices.items()])
    rows.append(row)

print('\n'.join(rows))
