import pandas as pd
import os
import time
from datetime import datetime

path = "./intraQuarter"


def key_stats(gather="Total Debt/Equity (mrq)"):
    stats_path = path + "/_KeyStats"
    stock_list = [stock[0] for stock in os.walk(stats_path)]

    df = pd.DataFrame(columns=["Date", "Unix", "Ticker", "DE Ratio", "Price", "SP500"])

    sp500_df = pd.read_csv("YAHOO-INDEX_GSPC.csv")

    # Loop over stocks in S&P 500
    for stock_dir in stock_list[1:]:
        stock_files = os.listdir(stock_dir)
        ticker = stock_dir.split(stats_path + "/")[1]

        if len(stock_files) == 0:
            continue

        # Loop over records over time for a given stock
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

                stock_price = source_code.split("</small><big><b>")[1].split(
                    "</b></big>"
                )[0]

                try:
                    # Parse S&P 500 value for the given date
                    sp500_date = datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d")
                    row = sp500_df[sp500_df["Date"] == sp500_date]
                    if len(row) == 0:
                        continue
                    sp500_value = float(row["Adj Close"])
                except:
                    # Look 3 days before if no data found
                    sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime(
                        "%Y-%m-%d"
                    )
                    row = sp500_df[sp500_df["Date"] == sp500_date]
                    sp500_value = float(row["Adj Close"])

                df = df.append(
                    {
                        "Date": date_stamp,
                        "Unix": unix_time,
                        "Ticker": ticker,
                        "DE Ratio": value,
                        "Price": stock_price,
                        "SP500": sp500_value,
                    },
                    ignore_index=True,
                )

            except Exception as e:
                print(
                    "caught exception with ticker: ",
                    ticker,
                    "full file path: ",
                    full_file_path,
                    # "value: ",
                    # value,
                    # "row: ",
                    # row,
                )
                pass

    save_path = (
        gather.replace(" ", "").replace("(", "").replace(")", "").replace("/", "")
        + ".csv"
    )

    df.to_csv(save_path)


key_stats()

