#!/usr/bin/env python

import sys
from datetime import datetime
import requests

ts_start = int(datetime(2019, 7, 31).timestamp())
ts_end = int(datetime.today().timestamp())

coins = ["bitcoin", "bitcoin-cash", "ethereum", "ripple", "litecoin", "origin-protocol", "filecoin", "zcash"]
all = {}
for coin in coins:
    sys.stderr.write(f"Getting prices for {coin}\n")
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
            sys.stderr.write(f"{ts.strftime('%Y-%m-%d')}	{price}\n")

#print(all)

rows =  ["date\t" + '\t'.join(coins)]
for ts, prices in all.items():
    row = f"{ts}\t"
    row += "\t".join([str(val) for _, val in prices.items()])
    rows.append(row)

print('\n'.join(rows))
sys.stderr.write("Done\n")
