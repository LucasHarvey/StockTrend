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
        regex = re.escape(kpi) + r".*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>"
        value = re.search(regex, source_code)
        value = value.group(1)

        if "B" in value:
            value = float(value.replace("B", "")) * 1000000000
        elif "M" in value:
            value = float(value.replace("M", "")) * 1000000

        return value

    except:
        return "N/A"


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


def key_stats(
    kpis=[
        "Total Debt/Equity",
        "Trailing P/E",
        "Price/Sales",
        "Price/Book",
        "Profit Margin",
        "Operating Margin",
        "Return on Assets",
        "Return on Equity",
        "Revenue Per Share",
        "Market Cap",
        "Enterprise Value",
        "Forward P/E",
        "PEG Ratio",
        "Enterprise Value/Revenue",
        "Enterprise Value/EBITDA",
        "Revenue",
        "Gross Profit",
        "EBITDA",
        "Net Income Avl to Common ",
        "Diluted EPS",
        "Earnings Growth",
        "Revenue Growth",
        "Total Cash",
        "Total Cash Per Share",
        "Total Debt",
        "Current Ratio",
        "Book Value Per Share",
        "Cash Flow",
        "Beta",
        "Held by Insiders",
        "Held by Institutions",
        "Shares Short (as of",
        "Short Ratio",
        "Short % of Float",
        "Shares Short (prior ",
    ]
):
    stats_path = path + "/_KeyStats"
    stock_list = [stock[0] for stock in os.walk(stats_path)]
    stock_list = sorted(stock_list)

    df = pd.DataFrame(
        columns=[
            "Date",
            "Unix",
            "Ticker",
            "Price",
            "stock_p_change",
            "SP500",
            "sp500_p_change",
            "Difference",
            ##############
            "DE Ratio",
            "Trailing P/E",
            "Price/Sales",
            "Price/Book",
            "Profit Margin",
            "Operating Margin",
            "Return on Assets",
            "Return on Equity",
            "Revenue Per Share",
            "Market Cap",
            "Enterprise Value",
            "Forward P/E",
            "PEG Ratio",
            "Enterprise Value/Revenue",
            "Enterprise Value/EBITDA",
            "Revenue",
            "Gross Profit",
            "EBITDA",
            "Net Income Avl to Common ",
            "Diluted EPS",
            "Earnings Growth",
            "Revenue Growth",
            "Total Cash",
            "Total Cash Per Share",
            "Total Debt",
            "Current Ratio",
            "Book Value Per Share",
            "Cash Flow",
            "Beta",
            "Held by Insiders",
            "Held by Institutions",
            "Shares Short (as of",
            "Short Ratio",
            "Short % of Float",
            "Shares Short (prior ",
            ##############
            "Status",
        ]
    )

    sp500_df = pd.read_csv("YAHOO-INDEX_GSPC.csv")

    tickers = []

    # Loop over stocks in S&P 500
    for stock_dir in stock_list[1:]:
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
                kpi_values = []

                for kpi in kpis:

                    # Get the KPI value we are interested in
                    kpi_value = get_kpi_from_source(kpi, source_code)
                    kpi_values.append(kpi_value)

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

                # Do not use stock if we have N/A values
                if kpi_values.count("N/A") > 0:
                    pass
                else:

                    df = df.append(
                        {
                            "Date": date_stamp,
                            "Unix": unix_time,
                            "Ticker": ticker,
                            "Price": stock_price,
                            "stock_p_change": stock_p_change,
                            "SP500": sp500_value,
                            "sp500_p_change": sp500_p_change,
                            "Difference": difference,
                            "DE Ratio": kpi_values[0],
                            #'Market Cap':kpi_values[1],
                            "Trailing P/E": kpi_values[1],
                            "Price/Sales": kpi_values[2],
                            "Price/Book": kpi_values[3],
                            "Profit Margin": kpi_values[4],
                            "Operating Margin": kpi_values[5],
                            "Return on Assets": kpi_values[6],
                            "Return on Equity": kpi_values[7],
                            "Revenue Per Share": kpi_values[8],
                            "Market Cap": kpi_values[9],
                            "Enterprise Value": kpi_values[10],
                            "Forward P/E": kpi_values[11],
                            "PEG Ratio": kpi_values[12],
                            "Enterprise Value/Revenue": kpi_values[13],
                            "Enterprise Value/EBITDA": kpi_values[14],
                            "Revenue": kpi_values[15],
                            "Gross Profit": kpi_values[16],
                            "EBITDA": kpi_values[17],
                            "Net Income Avl to Common ": kpi_values[18],
                            "Diluted EPS": kpi_values[19],
                            "Earnings Growth": kpi_values[20],
                            "Revenue Growth": kpi_values[21],
                            "Total Cash": kpi_values[22],
                            "Total Cash Per Share": kpi_values[23],
                            "Total Debt": kpi_values[24],
                            "Current Ratio": kpi_values[25],
                            "Book Value Per Share": kpi_values[26],
                            "Cash Flow": kpi_values[27],
                            "Beta": kpi_values[28],
                            "Held by Insiders": kpi_values[29],
                            "Held by Institutions": kpi_values[30],
                            "Shares Short (as of": kpi_values[31],
                            "Short Ratio": kpi_values[32],
                            "Short % of Float": kpi_values[33],
                            "Shares Short (prior ": kpi_values[34],
                            "Status": status,
                        },
                        ignore_index=True,
                    )

            except Exception as e:
                print(str(e))
                pass

    # Plot tickers
    # for ticker in tickers:
    #     try:
    #         plot_df = df[df["Ticker"] == ticker]
    #         plot_df = plot_df.set_index(["Date"])

    #         if plot_df["Status"][-1] == "underperform":
    #             color = "r"
    #         else:
    #             color = "g"

    #         plot_df["Difference"].plot(label=ticker, color=color)

    #         plt.legend()
    #     except:
    #         pass

    # plt.show()

    df.to_csv("key_stats.csv")


key_stats()

