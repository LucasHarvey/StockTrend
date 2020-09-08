import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
import pandas as pd
from matplotlib import style
import quandl
import statistics
from datetime import datetime
import os

style.use("ggplot")

FEATURES = [
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
]


def build_data_set():
    # data_df = pd.read_csv("key_stats.csv")
    data_df = pd.read_csv("key_stats_acc_perf_WITH_NA_enhanced.csv")

    data_df = data_df.reindex(np.random.permutation(data_df.index))
    data_df = data_df.fillna(0)

    # data_df = data_df[:50]

    X = np.array(data_df[FEATURES].values.tolist())
    y = data_df["Status"].values.tolist()

    # Normalization
    X = preprocessing.scale(X)

    Z = np.array(data_df[["stock_p_change", "sp500_p_change"]])

    return X, y, Z


def analysis():

    X, y, Z = build_data_set()

    print("dataset size: ", len(X))

    # test_size = 1000
    test_size = 1

    invest_amount = 10000
    total_invests = 0
    market_returns = 0
    strat_returns = 0

    training_X = X[:-test_size]
    training_y = y[:-test_size]

    test_X = X[-test_size:]
    test_y = y[-test_size:]
    test_Z = Z[-test_size:]

    clf = svm.SVC(kernel="linear", C=1.0)
    clf.fit(training_X, training_y)

    # Testing

    correct_count = 0
    for i in range(0, test_size):
        prediction = clf.predict(test_X[i].reshape(1, -1))[0]
        if prediction == test_y[i]:
            correct_count += 1
        if prediction == 1:
            # Make investment
            stock_change = Z[i][0] / 100
            strat_return = invest_amount + invest_amount * stock_change
            strat_returns += strat_return

            # Invest in market
            sp500_change = Z[i][1] / 100
            market_return = invest_amount + invest_amount * sp500_change
            market_returns += market_return

            total_invests += 1

    # print("Accuracy:", (correct_count / test_size) * 100)

    # print("Total Trades:", total_invests)
    # print("Returns From Strategy:", strat_returns)
    # print("Returns From Market:", market_returns)

    # compared = (strat_returns - market_returns) / market_returns * 100
    # no_investments = total_invests * invest_amount

    # avg_market_returns = (market_returns - no_investments) / no_investments * 100
    # avg_strat_returns = (strat_returns - no_investments) / no_investments * 100

    # print(str(compared), "% earned compared to market")
    # print("Average investment return:", str(avg_strat_returns), "%")
    # print("Average market return:", str(avg_market_returns), "%")

    today = datetime.today().strftime("%Y_%m_%d")
    today_path = os.path.join("./current_stats", today)
    if not os.path.exists(today_path):
        print("Data Not Found For Date:", today)
        return

    data_path = os.path.join(today_path, "compiled_stats_WITH_NA.csv")
    data_df = pd.read_csv(data_path)

    data_df = data_df.fillna(0)

    X = np.array(data_df[FEATURES].values.tolist())
    # Normalization
    X = preprocessing.scale(X)

    Z = np.array(data_df["Ticker"].values.tolist())

    investments = []

    for i in range(len(X)):
        p = clf.predict(X[i].reshape(1, -1))[0]
        if p == 1:
            stock = Z[i]
            print(stock)
            investments.append(stock)

    print("Total Investments:", len(investments))
    print("Investments:", investments)


analysis()

# COMMENTS ON STRATEGY
# - Does not take into account companies that are no longer in the S&P500 between in 2013
#   * These companies can weigh down the index up until 2013, but we don't invest in them
# - Instead of basing our results on model accuracy, we look at strategy performance compared to the market
