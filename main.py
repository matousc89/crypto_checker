import requests
import time
from datetime import datetime



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
    high = 30
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

def compile_html(targets, filename):
    # export in html
    html_template = """
     <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Crypto prices</title>
            <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/js/bootstrap.min.js" integrity="sha384-a5N7Y/aK3qNeh15eJKGWxsqtnX/wWdSZSKp+81YjTmS15nvnvxKHuzaWwXHDli+4" crossorigin="anonymous"></script>
            <style>
                {}
            </style>
        </head>
        <body>
            <h3>{}</h3>
            <nav>
                <a href="view_alpha.html">Alphabetical</a>&nbsp;|
                <a href="view_1D.html">1 day gain</a>&nbsp;|
                <a href="view_2D.html">2 days gain</a>&nbsp;|
                <a href="view_1W.html">1 week gain</a>
            </nav>
            <table>
                <tr>
                    <th>Symbol</th><th>1 day [%]</th><th>2 days [%]</th><th>1 week [%]</th><th>Status</th>
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
        cell_symbol = cell_template.format(symbol_style, target["symbol"])
        ch_1D = round(target["change_1D"], 2)
        ch_2D = round(target["change_2D"], 2)
        ch_1W = round(target["change_1W"], 2)
        cell_1D = cell_template.format(html_value_style(ch_1D), ch_1D)
        cell_2D = cell_template.format(html_value_style(ch_2D), ch_2D)
        cell_1W = cell_template.format(html_value_style(ch_1W), ch_1W)
        cell_status = cell_template.format("", target["status"])
        # create line and append it to content
        line = cell_symbol + cell_1D + cell_2D + cell_1W + cell_status
        html_content += line_template.format(line)
    # get date time
    heading = str(datetime.now())
    # put it together and save it
    html = html_template.format(css, heading, html_content)
    with open(filename, "w") as f:
        f.write(html)


targets = ["ARK","QSP","DGD","GTO","ADA","GVT","BCPT","TNB","OAX","BCD","KNC","SNGLS","BAT","DNT","BQX","NULS","ELF","CTR","POE","APPC","BNB","ZEC","ZRX","VIB","LUN","RDN","WABI","NEBL","OST","MANA","WINGS","CND","KMD","VEN","LSK","BRD","ADX","ICX","SUB","CDT","POWR","DLT","ARN","EDO","TNT","PPT","WTC","ETC","WAVES","DASH","NAV","TRIG","OMG","XVG","ICN","FUN","GXS","GXS","XMR","AMB","MTL","STORJ","HSR","NEO","XRP","LRC","MTH","ENG","EOS","YOYO","IOTA","BTS","QTUM","STRAT","XZC","AION","EVX","LINK","AST","SNM","SNT","SALT","TRX","BNT","ENJ"]
# targets = ["ETH", "GTO", "BTC"]
currency = "USD"

time_actual = time.time()
time_1D = time_actual - 3600*24
time_2D = time_actual - 3600*24*2
time_1W = time_actual - 3600*24*7


SCOPES = [
    {"name": "1D", "timestamp": time_actual - 3600*24},
    {"name": "2D", "timestamp": time_actual - 3600*24*2},
    {"name": "1W", "timestamp": time_actual - 3600*24*7},
]


# targets = targets[:3]

# store values in dictionary
items = []
for target in targets:
    time.sleep(0.1)
    print("Downloading: ", target)
    item = {
        "symbol": target,
        "price": 0,
        "status": "Ok",
    }
    for scope in SCOPES:
        item["price_"+scope["name"]] = 0
        item["change_" + scope["name"]] = 0
    # get price
    try:
        price_now = get_price(target, currency)[target][currency]
    except Exception as e:
        item["status"] = "Unable to get data - " + str(e)
    if price_now:
        # get other prices and calculate changes
        for scope in SCOPES:
            try:
                price = get_price(target, currency, scope["timestamp"])[target][currency]
                item["price_" + scope["name"]] = price
                change = (price_now / price * 100) - 100
                item["change_" + scope["name"]] = change
            except Exception as e:
                item["status"] = e
    # store it
    items.append(item)
    print(item["status"])


compile_html(items, "view_alpha.html")

items = sorted(items, key=lambda k: k['change_1D'], reverse=True)
compile_html(items, "view_1D.html")

items = sorted(items, key=lambda k: k['change_2D'], reverse=True)
compile_html(items, "view_2D.html")

items = sorted(items, key=lambda k: k['change_1W'], reverse=True)
compile_html(items, "view_1W.html")












