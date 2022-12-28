import matplotlib.pyplot as plt
import pandas as pd
import pickle

mymarkets = [
    "ETH-USD",
    "1INCH-USD",
    "AVAX-USD",
    "CRV-USD",
    "UNI-USD",
    "NEAR-USD",
    "COMP-USD",
]


def run_test(df_in, short_tickers, long_tickers, short_size, long_size):
    """Run a backtest on a dataframe"""
    """Requires column formatting 'TICKER price' and 'TICKER rate'"""
    df = df_in.astype(float).copy()
    short_item_weight = 1 / len(short_tickers)
    long_item_weight = 1 / len(long_tickers)
    df["shorts_value"] = short_size
    df["longs_value"] = long_size
    df["portfolio_value"] = short_size + long_size

    print("--------------------")
    print("Running Backtest")
    print("> Short tickers:", short_tickers)
    print("> Long tickers:", long_tickers)
    print("Portfolio value:", short_size + long_size)
    print("--------------------")

    prev = None
    for idx, row in df.iterrows():
        if prev is None:
            prev = row
            continue

        # calculate shorts
        short_day_factor = 0
        for ticker in short_tickers:
            if row[ticker + " price"] == 0:
                print("Found zero price, replacing with previous price")
                row[ticker + " price"] = prev[ticker + " price"]

            # hr_change = yesterday / today
            hr_change_short = prev[ticker + " price"] / row[ticker + " price"]

            # factor funding, positive funding -> shorts get paid
            hr_short_perf = hr_change_short * (1 + row[ticker + " rate"])
            # add to basket
            short_day_factor += (hr_short_perf) * short_item_weight

            # # logging for debugging
            # if short == "AVAX-USD":
            #     print("AVAX prev:", prev[short + " price"])
            #     print("AVAX today:", row[short + " price"])
            #     print("AVAX change:", hr_change_short)
            #     print("Hour Short perf:", (1 + hr_change_short))
            #     print("With funding:", hr_short_perf)

        # calculate longs
        long_day_factor = 0
        for ticker in long_tickers:
            # hr change = today / yesterday
            hr_change_long = row[ticker + " price"] / prev[ticker + " price"]
            # factor funding
            hr_long_perf = hr_change_long * (1 - row[ticker + " rate"])
            # add to basket
            long_day_factor += (hr_long_perf) * long_item_weight

        # # Sanity
        # print("ETH yesterday:", prev["ETH-USD price"])
        # print("ETH today:", row["ETH-USD price"])
        # print("Short Value Change:", short_day_factor)
        # print("Long Value Change:", long_day_factor)
        # print("Product should equal 1:", short_day_factor * long_day_factor)

        row.shorts_value = prev.shorts_value * short_day_factor
        row.longs_value = prev.longs_value * long_day_factor
        row.portfolio_value = row.shorts_value + row.longs_value

        # save changes to df
        df.loc[idx] = row
        prev = row

    return df


def to_csv():
    df = pd.read_pickle("../data/dydx/backtest-equal-short.pkl")
    df["portfolio_change"] = df["portfolio_value"].pct_change()

    df.to_csv("../data/dydx/backtest-equal-short.csv")
    # # df["RFR"] = 0.04 / (365 * 24)
    # # df["sharpe"] = (df["portfolio_change"] - df["RFR"]) / df["portfolio_change"].std()

    # print(df.head(5))

    # df.plot(
    #     y=["portfolio_value", "sharpe"],
    #     kind="line",
    #     title="DYDX Backtest \n Equal-Weight Short",
    # )

    # plt.show()


def chart_backtest():
    df = pd.read_pickle("../data/dydx/backtest-equal-short.pkl")

    # print(df.head(5))
    df.plot(
        y=["portfolio_value"],
        ylabel="$ millions",
        kind="line",
        title="DYDX Backtest \n Long ETH || Equal-Weight Short 1INCH, AVAX, CRV, UNI, NEAR, COMP",
    )
    plt.show()

    # # save backtest
    # plt.savefig(
    #     "dydx-equal-weight",
    #     dpi=300,
    #     format="png",
    # )


def backtest_equal_short():
    """Backtest equal weight short strategy"""

    df = pd.read_pickle("../data/dydx/funding/combined.pkl")

    # # SANITY CHECK
    # test_df = df.iloc[:10].copy()
    # shorts = [mymarkets[0]]
    # longs = shorts
    # backtest = run_test(test_df, shorts, longs, 500000, 500000)

    shorts = mymarkets[1:]
    longs = [mymarkets[0]]
    backtest = run_test(df, shorts, longs, 500000, 500000)

    print(backtest.head(5))
    print(backtest.tail(5))

    backtest.to_pickle("../data/dydx/backtest-equal-short.pkl")

    # # add a new column of 0s to the dataframe
    # df["shorts_value"] = 500000
    # df["longs_value"] = 500000

    # # print(df.head(3))

    # df = df.astype(float).copy()

    # short_df = df.iloc[:3].copy()

    # print(short_df.head(3))
    # backtest = run_test(short_df)
    # print(backtest.head(3))

    # short_df.apply(compute_value_equal_short, axis=1)

    # print(short_df.head(3))

    # hello

    # print(df.head())

    # print(df["shorts_value"])

    # df["shorts_value"] = df.apply(compute_value_equal_short, axis=1)

    # df["shorts_value"] = df["shorts_value"].shift(1) * df["1INCH-USD price"]

    # print(df.head())


# backtest_equal_short()
# chart_backtest()
compute_sharpe()
