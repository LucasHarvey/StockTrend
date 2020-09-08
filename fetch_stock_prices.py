import pandas as pd
import os
import quandl
import time

quandl.ApiConfig.api_key = "EBc8AqCWKJNbuzXRzVP_"

data = quandl.get("WIKI/KO", trim_start="2000-12-12", trim_end="2014-12-30")

df = pd.DataFrame()
data["KO"] = data["Adj. Close"]
# print(data)
df = pd.concat([df, data["KO"]], axis=1)
print(df)


path = "./intraQuarter/"


def get_stock_price(ticker):
    name = "WIKI/" + ticker
    data = quandl.get(name, trim_start="2000-12-12", trim_end="2014-12-30")
    data[ticker] = data["Adj. Close"]
    return data


def get_stock_prices():
    df = pd.DataFrame()
    stock_prices_path = path + "_KeyStats"
    stocks = [x[0] for x in os.walk(stock_prices_path)]
    stocks = sorted(stocks)

    for stock in stocks[1:]:
        ticker = stock.split("/")[3]
        print(ticker)
        try:
            data = get_stock_price(ticker.upper())
            df = pd.concat([df, data[ticker.upper()]], axis=1)

        except Exception as e:
            print(str(e))
            time.sleep(10)
            # Try again in case API call failed
            try:
                data = get_stock_price(ticker.upper())
                df = pd.concat([df, data[ticker.upper()]], axis=1)
            except Exception as e:
                print(str(e))

    df.to_csv("stock_prices.csv")


# get_stock_prices()
