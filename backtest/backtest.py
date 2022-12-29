import matplotlib.pyplot as plt
import pandas as pd
import pickle

dydx_markets = [
    "ETH-USD",
    "1INCH-USD",
    "AVAX-USD",
    "CRV-USD",
    "UNI-USD",
    "NEAR-USD",
    "COMP-USD",
]

binance_markets = [
    "BTCBUSD",
    "ETHBUSD",
    "BNBBUSD",
    "SANDBUSD",
    "GMTBUSD",
    "NEARBUSD",
    "AVAXBUSD",
    "AXSUSDT",
    "CRVUSDT",
    "HNTUSDT",
    "DYDXUSDT",
    "1INCHUSDT",
    "FLOWUSDT",
]


def run_test(df_in, strategy, days=None):
    """Run a backtest on a dataframe"""
    """Requires column formatting 'TICKER price' and 'TICKER rate'"""
    df = df_in.astype(float).copy()

    if days and days * 24 < len(df):
        df = df.tail(days * 24)

    df["short_side"] = strategy["short_side"]["value"]
    df["long_side"] = strategy["long_side"]["value"]

    print("--------------------")
    print("Running Backtest")
    print("> Short Side: \n", strategy["short_side"]["tickers"])
    print("> Long Side: \n", strategy["long_side"]["tickers"])
    print(
        "Portfolio value:",
        strategy["short_side"]["value"] + strategy["long_side"]["value"],
    )
    print("--------------------")

    prev = None
    for idx, row in df.iterrows():
        if prev is None:
            prev = row
            continue

        # calculate shorts
        short_day_factor = 0
        for ticker, weight in strategy["short_side"]["tickers"].items():
            if row[ticker + " price"] == 0:
                print("Found zero price, filling with previous")
                row[ticker + " price"] = prev[ticker + " price"]

            # hr_change = yesterday / today
            hr_change_short = prev[ticker + " price"] / row[ticker + " price"]
            # factor funding, positive funding -> shorts get paid
            hr_short_perf = hr_change_short * (1 + row[ticker + " rate"])
            # add to basket
            short_day_factor += (hr_short_perf) * weight

        # calculate longs
        long_day_factor = 0
        for ticker, weight in strategy["long_side"]["tickers"].items():
            if row[ticker + " price"] == 0:
                print("Found zero price, filling with previous")
                row[ticker + " price"] = prev[ticker + " price"]

            # hr change = today / yesterday
            hr_change_long = row[ticker + " price"] / prev[ticker + " price"]
            # factor funding
            hr_long_perf = hr_change_long * (1 - row[ticker + " rate"])
            # add to basket
            long_day_factor += (hr_long_perf) * weight

        row.short_side = prev.short_side * short_day_factor
        row.long_side = prev.long_side * long_day_factor

        # # Sanity logging
        # print("ETH yesterday:", prev["ETH-USD price"])
        # print("ETH today:", row["ETH-USD price"])
        # print("Short Value Change:", short_day_factor)
        # print("Long Value Change:", long_day_factor)
        # print("Product should equal 1:", short_day_factor * long_day_factor)

        # save changes to df
        df.loc[idx] = row
        prev = row

    df["portfolio_value"] = df["short_side"] + df["long_side"]
    return df


def to_csv(df, file_path):
    # add hourly change
    df["portfolio_change"] = df["portfolio_value"].pct_change()
    # save
    df.to_csv(f"{file_path}.csv")


def chart_backtest(df, columns, title):
    df.plot(
        y=columns,
        ylabel="$ millions",
        kind="line",
        title=title,
    )
    plt.show()


def title_strategy(strategy):
    longs = "Long Side: "
    for ticker, weight in strategy["long_side"]["tickers"].items():
        asset = ticker[0 : len(ticker) - 4]
        longs += f"{asset} {weight} "
    shorts = "Short Side: "
    for ticker, weight in strategy["short_side"]["tickers"].items():
        asset = ticker[0 : len(ticker) - 4]
        shorts += f"{asset} {weight} "
    title = "Spread Strategy\n" + longs + "\n" + shorts
    return title


def perform_backtest():
    """Perform backtest on data"""

    df = pd.read_pickle("../store/data/binance/master_df.pkl")

    binance_strategy_map = {
        "long_side": {"value": 500000, "tickers": {"BTCBUSD": 0.2, "ETHBUSD": 0.8}},
        "short_side": {
            "value": 500000,
            "tickers": {
                "BNBBUSD": 0.1,
                "SANDBUSD": 0.1,
                "GMTBUSD": 0.1,
                "DYDXUSDT": 0.1,
                "AVAXBUSD": 0.1,
                "CRVUSDT": 0.1,
                "APTBUSD": 0.1,
                "HBARUSDT": 0.1,
                "ALGOUSDT": 0.1,
                "OPUSDT": 0.1,
                "NEARBUSD": 0.08,
                "AXSUSDT": 0.08,
                "1INCHUSDT": 0.08,
                "FLOWUSDT": 0.08,
            },
        },
    }
    title = title_strategy(binance_strategy_map)
    file_path = "../store/results/"

    backtest = run_test(df, binance_strategy_map, 90)

    print("--------------------")
    print("> backtest complete")
    print(backtest.head(5))
    chart_backtest(
        backtest, ["short_side", "long_side", "portfolio_value"], title=title
    )

    save_test = input("Would you like to export this test to csv? (y/n): ")
    if save_test == "y":
        name = input("Enter the name of the strategy: ")
        backtest.to_pickle(f"{file_path}tests/{name}.pkl")
        to_csv(backtest, f"{file_path}csv/{name}")


perform_backtest()

# def backtest_equal_short(df, name, short_markets, long_markets):
#     """Backtest equal weight short strategy"""
#     # # SANITY CHECK
#     # test_df = df.iloc[:10].copy()
#     # shorts = [mymarkets[0]]
#     # longs = shorts
#     # backtest = run_test(test_df, shorts, longs, 500000, 500000)

#     backtest = run_test(df, short_markets, long_markets, 500000, 500000)

#     print("BACKTEST RESULTS")
#     print(backtest.head(5))
#     print(backtest.tail(5))

#     backtest.to_pickle(f"../store/results/{name}.pkl")


# # df = pd.read_pickle("../data/dydx/funding/combined.pkl")
# # short_markets = dydx_markets[1:]
# # long_markets = dydx_markets[0:1]

# df = pd.read_pickle("../store/data/binance/master_df.pkl")
# name = "binance-equal-spread"
# short_markets = binance_markets[2:]
# long_markets = binance_markets[0:2]
# backtest_equal_short(df, name, short_markets, long_markets)

# # df = pd.read_pickle("../data/dydx/backtest-equal-short.pkl")
# df = pd.read_pickle(f"../store/results/{name}.pkl")
# title = f"Binance Backtest \n Equal-Weight Long: {', '.join(long_markets)} \n Equal-Weight Short: {', '.join(short_markets)}"
# chart_backtest(df, ["shorts_value", "longs_value", "portfolio_value"], title)


# df = pd.read_pickle("../data/dydx/backtest-equal-short.pkl")
# to_csv(df, "dydx-backtest-equal-weight")
