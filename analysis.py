import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing
import pandas as pd
from matplotlib import style
import quandl

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
    data_df = pd.read_csv("key_stats_acc_perf_NO_NA.csv")

    data_df = data_df.reindex(np.random.permutation(data_df.index))

    # data_df = data_df[:50]

    X = np.array(data_df[FEATURES].values.tolist())
    y = (
        data_df["Status"]
        .replace("underperform", 0)
        .replace("outperform", 1)
        .values.tolist()
    )

    # Normalization
    X = preprocessing.scale(X)

    return X, y


def analysis():

    X, y = build_data_set()

    print("dataset size: ", len(X))

    test_size = 1000

    training_X = X[:-test_size]
    training_y = y[:-test_size]

    test_X = X[-test_size:]
    test_y = y[-test_size:]

    clf = svm.SVC(kernel="linear", C=1.0)
    clf.fit(training_X, training_y)

    # Testing

    correct_count = 0
    for i in range(0, test_size):
        if clf.predict(test_X[i].reshape(1, -1))[0] == test_y[i]:
            correct_count += 1

    print("Accuracy:", (correct_count / test_size) * 100)

    # Graph

    # w = clf.coef_[0]
    # a = -w[0] / w[1]

    # xx = np.linspace(min(X[:, 0]), max(X[:, 0]))
    # yy = a * xx - clf.intercept_[0] / w[1]

    # h0 = plt.plot(xx, yy, "k-", label="non weighted")

    # plt.scatter(X[:, 0], X[:, 1], c=y)
    # plt.ylabel("Trailing P/E")
    # plt.xlabel("DE Ratio")

    # plt.show()


analysis()
