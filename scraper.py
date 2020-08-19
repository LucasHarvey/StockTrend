import pandas as pd
import os
import time
from datetime import datetime

path = "./intraQuarter"


def key_stats(gather="Total Debt/Equity (mrq)"):
    stats_path = path + "/_KeyStats"
    stock_list = [stock[0] for stock in os.walk(stats_path)]

    df = pd.DataFrame(columns=["Date", "Unix", "Ticker", "DE Ratio"])

    for stock_dir in stock_list[1:]:
        stock_files = os.listdir(stock_dir)
        ticker = stock_dir.split(stats_path + "/")[1]

        if len(stock_files) == 0:
            continue
        for stock_file in stock_files:
            date_stamp = datetime.strptime(stock_file, "%Y%m%d%H%M%S.html")
            unix_time = time.mktime(date_stamp.timetuple())

            full_file_path = stock_dir + "/" + stock_file

            source_code = open(full_file_path, "r").read()

            try:

                value = float(
                    source_code.split(gather + ':</td><td class="yfnc_tabledata1">')[
                        1
                    ].split("</td>")[0]
                )

                df = df.append(
                    {
                        "Date": date_stamp,
                        "Unix": unix_time,
                        "Ticker": ticker,
                        "DE Ratio": value,
                    },
                    ignore_index=True,
                )

            except Exception as e:
                pass

    save_path = (
        gather.replace(" ", "").replace("(", "").replace(")", "").replace("/", "")
        + ".csv"
    )

    df.to_csv(save_path)


key_stats()

