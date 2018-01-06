import requests
import time



def get_price(target, currency, timestamp=False):
    timestamp = int(timestamp)
    if timestamp:
        base_url = "https://min-api.cryptocompare.com/data/pricehistorical"
        params = "?fsym={}&tsyms={}&ts={}".format(target, currency, timestamp)
    else:
        base_url = "https://min-api.cryptocompare.com/data/pricemulti"
        params = "?fsyms={}&tsyms={}".format(target, currency)
    url = base_url + params
    r = requests.get(url)
    if not r.status_code == 200:
        raise Exception("Cryptocompare does not return status 200")
    return r.json()

def html_value_style(value):
    high = 5
    ultra_high = 100
    if value > ultra_high:
        return "positive important highlight"
    if value > high:
        return "positive important"
    elif value < -high:
        return "negative important"
    elif value > 0:
        return "positive"
    elif value < 0:
        return "negative"


targets = ["ARK","ARK","QSP","DGD","GTO","ADA","GVT","BCPT","TNB","OAX","BCD","KNC","SNGLS","BAT","DNT","BQX","NULS","ELF","CTR","POE","APPC","BNB","ZEC","ZRX","VIB","LUN","RDN","WABI","NEBL","OST","MANA","WINGS","CND","KMD","VEN","LSK","BRD","ADX","ICX","SUB","CDT","POWR","DLT","ARN","EDO","TNT","PPT","WTC","ETC","WAVES","DASH","NAV","TRIG","OMG","XVG","ICN","FUN","GXS","GXS","XMR","AMB","MTL","STORJ","HSR","NEO","XRP","LRC","MTH","ENG","EOS","YOYO","IOTA","BTS","QTUM","STRAT","XZC","AION","EVX","LINK","AST","SNM","SNT","SALT","TRX","BNT","ENJ"]
currency = "USD"

time_actual = time.time()
time_1D = time_actual - 3600*24
time_2D = time_actual - 3600*24*2


# store values in dictionary
out = {}
for target in targets:
    time.sleep(0.1)
    print("Downloading: ", target)
    try:
        # get prices
        price_now = get_price(target, currency)[target][currency]
        price_1D = get_price(target, currency, time_1D)[target][currency]
        price_2D = get_price(target, currency, time_2D)[target][currency]
        # calculate changes in percents 24h, 48h
        change_1D = (price_now / price_1D * 100) - 100
        change_2D = (price_now / price_2D * 100) - 100
        # store it
        values = {
            "price": price_now,
            "price_1D": price_1D,
            "price_2D": price_2D,
            "change_1D": change_1D,
            "change_2D": change_2D,
            "status": "Ok"
        }
        out[target] = values
        print("Done.")
    except Exception as e:
        print(e)
        # store it
        values = {
            "price": 0,
            "price_1D": 0,
            "price_2D": 0,
            "change_1D": 0,
            "change_2D": 0,
            "status": e,
        }
        out[target] = values


# export in html
html_template = """
 <!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>Crypto prices</title>
        <style>
            {}
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>Symbol</th><th>24 hours [%]</th><th>48 hours [%]</th><th>Status</th>
            </tr>
            {}
        </table>
    </body>
</html> 
"""
css = """
            .positive {
                color: green;
            }
            .negative {
                color: red;
            }
            .important {
                font-weight: bold;
            }
            .highlight {
                background-color: yellow;
            }
            
"""
line_template = """
            <tr>
                {}
            </tr>
"""
cell_template = '<td class="{}">{}</td>'
html_content = ""
symbol_style = ""
for target in targets:
    # cells
    cell_symbol = cell_template.format(symbol_style, target)
    ch_1D = round(out[target]["change_1D"], 2)
    ch_2D = round(out[target]["change_2D"], 2)
    cell_1D = cell_template.format(html_value_style(ch_1D), ch_1D)
    cell_2D = cell_template.format(html_value_style(ch_2D), ch_2D)
    cell_status = cell_template.format("", out[target]["status"])
    # create line and append it to content
    line = cell_symbol + cell_1D + cell_2D + cell_status
    html_content += line_template.format(line)

html = html_template.format(css, html_content)
with open("index.html", "w") as f:
    f.write(html)














