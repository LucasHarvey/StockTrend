import urllib.request
import os
import time
from datetime import datetime

path = "./intraQuarter"


def check_yahoo():

    today = datetime.today().strftime("%Y_%m_%d")
    today_path = "./current_stats/" + today
    if not os.path.exists(today_path):
        os.mkdir(today_path)

    stats_path = os.path.join(path, "_KeyStats")
    stock_paths = [x[0] for x in os.walk(stats_path)]
    stock_paths = sorted(stock_paths)
    for stock_path in stock_paths[1:]:
        try:
            stock = stock_path.split("/")[-1]
            ticker = stock.upper()
            print(ticker)
            link = (
                "https://finance.yahoo.com/quote/"
                + ticker
                + "/key-statistics?p="
                + ticker
            )

            resp = urllib.request.urlopen(link).read()

            save_loc = os.path.join(today_path, str(stock) + ".html")

            f = open(save_loc, "w")
            f.write(str(resp))
            f.close()

        except Exception as e:
            print(e)
            time.sleep(5)


check_yahoo()
