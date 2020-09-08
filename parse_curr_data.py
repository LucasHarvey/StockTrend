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


def compile_curr_stats(
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

    today = datetime.today().strftime("%Y_%m_%d")
    today_path = os.path.join("./current_stats", today)
    if not os.path.exists(today_path):
        print("Data Not Found For Date:", today)
        return

    stock_files = os.listdir(today_path)
    stock_files = sorted(stock_files)

    for stock_file in stock_files:

        ticker = stock_file.split(".html")[0]
        print(ticker)
        full_path = os.path.join(today_path, stock_file)
        source_code = open(full_path, "r").read()

        try:
            kpi_values = []

            for kpi in kpis:

                # Get the KPI value we are interested in
                kpi_value = get_kpi_from_source(kpi, source_code)
                kpi_values.append(kpi_value)

            # Do not use stock if we have N/A values
            if kpi_values.count("N/A") > 15:
                pass
            else:

                df = df.append(
                    {
                        "Date": today,
                        "Unix": "N/A",
                        "Ticker": ticker,
                        "Price": "N/A",
                        "stock_p_change": "N/A",
                        "SP500": "N/A",
                        "sp500_p_change": "N/A",
                        "Difference": "N/A",
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
                        "Status": "N/A",
                    },
                    ignore_index=True,
                )

        except Exception as e:
            print(str(e))
            pass

    save_loc = os.path.join(today_path, "compiled_stats_WITH_NA.csv")
    df.to_csv(save_loc)


compile_curr_stats()

