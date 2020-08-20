import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

style.use("dark_background")

import re

path = "./intraQuarter"


def key_stats(gather="Total Debt/Equity (mrq)"):
    stats_path = path + "/_KeyStats"
    stock_list = [stock[0] for stock in os.walk(stats_path)]
    stock_list = sorted(stock_list)

    df = pd.DataFrame(
        columns=[
            "Date",
            "Unix",
            "Ticker",
            "DE Ratio",
            "Price",
            "stock_p_change",
            "SP500",
            "sp500_p_change",
            "Difference",
        ]
    )

    sp500_df = pd.read_csv("YAHOO-INDEX_GSPC.csv")

    tickers = []

    # Loop over stocks in S&P 500
    for stock_dir in stock_list[1:25]:
        stock_files = os.listdir(stock_dir)
        # VERY Important! Sort stock files in chronological order
        stock_files = sorted(stock_files)
        ticker = stock_dir.split(stats_path + "/")[1]
        tickers.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        if len(stock_files) == 0:
            continue

        # Loop over records over time for a given stock
        for stock_file in stock_files:
            date_stamp = datetime.strptime(stock_file, "%Y%m%d%H%M%S.html")
            unix_time = time.mktime(date_stamp.timetuple())

            full_file_path = stock_dir + "/" + stock_file

            source_code = open(full_file_path, "r").read()

            try:

                try:
                    value = float(
                        source_code.split(
                            gather + ':</td><td class="yfnc_tabledata1">'
                        )[1].split("</td>")[0]
                    )
                except:
                    # Formatting changed
                    try:
                        value = float(
                            source_code.split(
                                gather + ':</td>\n<td class="yfnc_tabledata1">'
                            )[1].split("</td>")[0]
                        )
                    except Exception as e:
                        # Value is N/A
                        pass

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

                try:
                    stock_price = float(
                        source_code.split("</small><big><b>")[1].split("</b></big>")[0]
                    )

                except:

                    try:
                        stock_price = source_code.split("</small><big><b>")[1].split(
                            "</b></big>"
                        )[0]

                        stock_price = re.search(r"(\d{1,8}\.\d{1,8})", stock_price)
                        stock_price = float(stock_price.group(1))
                        # print(stock_price)
                    except Exception as e:
                        # real-time ticker
                        stock_price = source_code.split(
                            '<span class="time_rtq_ticker">'
                        )[1].split("</span>")[0]
                        stock_price = re.search(r"(\d{1,8}\.\d{1,8})", stock_price)
                        stock_price = float(stock_price.group(1))
                        # print("Latest:", stock_price)
                        # print("stock price", str(e), ticker, stock_file)
                        # time.sleep(15)

                if not starting_stock_value:
                    starting_stock_value = stock_price
                if not starting_sp500_value:
                    starting_sp500_value = sp500_value

                stock_p_change = (
                    (stock_price - starting_stock_value) / starting_stock_value
                ) * 100

                sp500_p_change = (
                    (sp500_value - starting_sp500_value) / starting_sp500_value
                ) * 100

                df = df.append(
                    {
                        "Date": date_stamp,
                        "Unix": unix_time,
                        "Ticker": ticker,
                        "DE Ratio": value,
                        "Price": stock_price,
                        "stock_p_change": stock_p_change,
                        "SP500": sp500_value,
                        "sp500_p_change": sp500_p_change,
                        "Difference": stock_p_change - sp500_p_change,
                    },
                    ignore_index=True,
                )

            except Exception as e:
                print(str(e))
                # print(
                #     "caught exception with ticker: ",
                #     ticker,
                #     "full file path: ",
                #     full_file_path,
                #     # "value: ",
                #     # value,
                #     # "row: ",
                #     # row,
                # )
                pass

    for ticker in tickers:
        try:
            plot_df = df[df["Ticker"] == ticker]
            plot_df = plot_df.set_index(["Date"])
            plot_df["Difference"].plot(label=ticker)
            plt.legend()
        except:
            pass

    plt.show()

    save_path = (
        gather.replace(" ", "").replace("(", "").replace(")", "").replace("/", "")
        + ".csv"
    )

    df.to_csv(save_path)


key_stats()

