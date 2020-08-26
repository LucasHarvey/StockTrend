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


def get_kpi_from_source(kpi, source_code):
    try:
        value = float(
            source_code.split(kpi + ':</td><td class="yfnc_tabledata1">')[1].split(
                "</td>"
            )[0]
        )
        return value
    except:
        # Formatting changed
        try:
            value = float(
                source_code.split(kpi + ':</td>\n<td class="yfnc_tabledata1">')[
                    1
                ].split("</td>")[0]
            )
            return value
        except:
            # Value is N/A
            return False


def get_sp500_value_at_date(unix_time, sp500_df):
    try:
        # Parse S&P 500 value for the given date
        sp500_date = datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d")
        row = sp500_df[sp500_df["Date"] == sp500_date]
        if len(row) == 0:
            return False
        sp500_value = float(row["Adj Close"])
        return sp500_value
    except:
        # Look 3 days before if no data found
        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime("%Y-%m-%d")
        row = sp500_df[sp500_df["Date"] == sp500_date]
        sp500_value = float(row["Adj Close"])
        return sp500_value


def get_stock_price(source_code):
    try:
        stock_price = float(
            source_code.split("</small><big><b>")[1].split("</b></big>")[0]
        )
        return stock_price

    except:
        try:
            stock_price = source_code.split("</small><big><b>")[1].split("</b></big>")[
                0
            ]

            stock_price = re.search(r"(\d{1,8}\.\d{1,8})", stock_price)
            stock_price = float(stock_price.group(1))
            return stock_price
        except:
            # real-time ticker
            stock_price = source_code.split('<span class="time_rtq_ticker">')[1].split(
                "</span>"
            )[0]
            stock_price = re.search(r"(\d{1,8}\.\d{1,8})", stock_price)
            stock_price = float(stock_price.group(1))
            return stock_price


def key_stats(kpi="Total Debt/Equity (mrq)"):
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
            "Status",
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

                # Get the KPI value we are interested in
                kpi_value = get_kpi_from_source(kpi, source_code)

                # Get the SP500 value
                sp500_value = get_sp500_value_at_date(unix_time, sp500_df)
                if not sp500_value:
                    continue

                stock_price = get_stock_price(source_code)

                # Set initial values for starting prices
                if not starting_stock_value:
                    starting_stock_value = stock_price
                if not starting_sp500_value:
                    starting_sp500_value = sp500_value

                # Calculate price change for stock
                stock_p_change = (
                    (stock_price - starting_stock_value) / starting_stock_value
                ) * 100

                # Calculate price change for SP500
                sp500_p_change = (
                    (sp500_value - starting_sp500_value) / starting_sp500_value
                ) * 100

                difference = stock_p_change - sp500_p_change

                if difference > 0:
                    status = "outperform"
                else:
                    status = "underperform"

                df = df.append(
                    {
                        "Date": date_stamp,
                        "Unix": unix_time,
                        "Ticker": ticker,
                        "DE Ratio": kpi_value,
                        "Price": stock_price,
                        "stock_p_change": stock_p_change,
                        "SP500": sp500_value,
                        "sp500_p_change": sp500_p_change,
                        "Difference": difference,
                        "Status": status,
                    },
                    ignore_index=True,
                )

            except Exception as e:
                print(str(e))
                pass

    # Plot tickers
    for ticker in tickers:
        try:
            plot_df = df[df["Ticker"] == ticker]
            plot_df = plot_df.set_index(["Date"])

            if plot_df["Status"][-1] == "underperform":
                color = "r"
            else:
                color = "g"

            plot_df["Difference"].plot(label=ticker, color=color)

            plt.legend()
        except:
            pass

    plt.show()

    save_path = (
        kpi.replace(" ", "").replace("(", "").replace(")", "").replace("/", "") + ".csv"
    )

    df.to_csv(save_path)


key_stats()

