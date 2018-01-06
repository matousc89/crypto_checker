source = """
2018-01-05 20:15:45	ARKETH
"""


import time
import datetime
import json

lines = source.split("\n")


with open("trades.dat", "r") as f:
    assets_str = f.read()
    if assets_str:
        assets = json.loads(assets_str)
    else:
        assets = []

for line in lines:
    if line:
        cells = line.split("\t")
        date_cell = cells[0]
        symbol_cell = cells[1].replace("ETH", "")
        ts = int(time.mktime(datetime.datetime.strptime(date_cell, "%Y-%m-%d %H:%M:%S").timetuple()))
        # check if exists
        exists = False
        for asset in assets:
            if asset["symbol"] == symbol_cell:
                exists = True
                asset["timestamp"] = max(int(asset["timestamp"]), ts)
                break
        if not exists:
            new_asset = {
                "symbol": symbol_cell,
                "timestamp": ts,
            }
            assets.append(new_asset)

print(assets)

with open("trades.dat", "w") as f:
    f.write(json.dumps(assets, indent=4))







