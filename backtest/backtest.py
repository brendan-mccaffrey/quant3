import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

dydx_markets = [
    "ETH-USD",
    "1INCH-USD",
    "AVAX-USD",
    "CRV-USD",
    "UNI-USD",
    "NEAR-USD",
    "COMP-USD",
]

binance_tickers = [
    "BTCBUSD",
    "ETHBUSD",
    "BNBBUSD",
    "SANDBUSD",
    "GMTBUSD",
    "NEARBUSD",
    "AVAXBUSD",
    "AXSUSDT",
    "CRVUSDT",
    "HBARUSDT",
    "DYDXUSDT",
    "1INCHUSDT",
    "FLOWUSDT",
    "APTBUSD",
    "ALGOUSDT",
    "OPUSDT",
]


def run_test(df_in, strategy, days=None):
    """Run a backtest on a dataframe"""
    """Requires column formatting 'TICKER price' and 'TICKER rate'"""
    df = df_in.astype(float).copy()

    if days and days * 24 < len(df):
        df = df.tail(days * 24)

    df["short_side"] = strategy["short_side"]["value"]
    df["long_side"] = strategy["long_side"]["value"]

    # print("--------------------")
    # print("Running Backtest")
    # print("> Short Side: \n", strategy["short_side"]["tickers"])
    # print("> Long Side: \n", strategy["long_side"]["tickers"])
    # print(
    #     "Portfolio value:",
    #     strategy["short_side"]["value"] + strategy["long_side"]["value"],
    # )
    # print("--------------------")
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

        # if short_day_factor > 1.05:
        #     print("Large short change detected: ", short_day_factor)
        #     print(prev)
        #     print(row)

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


def make_strategy_with_weights(long_weights, short_weights):
    long_side = {
        "tickers": {},
        "value": 500000,
    }
    short_side = {
        "tickers": {},
        "value": 500000,
    }

    for i, weight in enumerate(long_weights):
        long_side["tickers"][binance_tickers[i]] = weight

    for i, weight in enumerate(short_weights):
        short_side["tickers"][binance_tickers[i + 2]] = weight

    strategy = {
        "long_side": long_side,
        "short_side": short_side,
    }

    return strategy


def sample_strategies():
    port_returns = []
    port_volatility = []
    port_weights = []

    num_assets = len(binance_tickers)
    num_portfolios = 100
    df = pd.read_pickle("../store/data/binance/data_df.pkl")

    var_matrix = pd.read_pickle("../store/data/binance/var_matrix.pkl")

    for port in range(num_portfolios):
        # calc random weights
        long_weights = np.random.random(2)
        short_weights = np.random.random(num_assets - 2)

        # normalize weights
        long_weights /= np.sum(long_weights)
        short_weights /= np.sum(short_weights)
        weights = np.concatenate([long_weights, short_weights])

        var_weights = np.concatenate([long_weights, [-x for x in short_weights]])

        port_weights.append(weights)

        strat = make_strategy_with_weights(long_weights, short_weights)
        backtest = run_test(df, strat)

        returns = (
            backtest["portfolio_value"].iloc[-1] / backtest["portfolio_value"].iloc[0]
            - 1
        )
        ann_returns = (1 + returns) ** (365 * 24 / len(backtest)) - 1
        port_returns.append(returns)

        var = var_matrix.mul(var_weights, axis=0).mul(var_weights, axis=1).sum().sum()
        sd = np.sqrt(var)

        ann_sd = sd * np.sqrt(365 * 24)
        port_volatility.append(ann_sd)

    data = {"Returns": port_returns, "Volatility": port_volatility}
    for counter, symbol in enumerate(binance_tickers):
        data[symbol + " weight"] = [w[counter] for w in port_weights]
    portfolios = pd.DataFrame(data)

    portfolios.sort_values(by="Returns", ascending=False, inplace=True)

    portfolios.to_pickle("../store/data/binance/portfolios_sample.pkl")
    print(df.head(10))

    portfolios.plot.scatter(
        x="Volatility",
        y="Returns",
        marker="o",
        color="r",
        s=15,
        alpha=0.5,
        figsize=(10, 8),
        grid=True,
    )
    plt.show()


def sanity_check(strategy):
    short_weight = sum(strategy["short_side"]["tickers"].values())
    long_weight = sum(strategy["long_side"]["tickers"].values())

    if not math.isclose(short_weight, 1):
        print(short_weight)
        raise ValueError("Short weight not 1")

    if not math.isclose(long_weight, 1):
        print(long_weight)
        raise ValueError("Long weight not 1")


def perform_backtest(df=None, strategy=None):
    """Perform backtest on data"""

    if df is None:
        df = pd.read_pickle("../store/data/binance/data_df.pkl")

    if strategy is None:
        strategy = {
            "long_side": {"value": 500000, "tickers": {"BTCBUSD": 0.1, "ETHBUSD": 0.9}},
            "short_side": {
                "value": 500000,
                "tickers": {
                    "BNBBUSD": 0.05,
                    "SANDBUSD": 0.1,
                    "GMTBUSD": 0.08,
                    "DYDXUSDT": 0.07,
                    "AVAXBUSD": 0.05,
                    "CRVUSDT": 0.06,
                    "APTBUSD": 0.12,
                    "HBARUSDT": 0.05,
                    "ALGOUSDT": 0.06,
                    "OPUSDT": 0.14,
                    "NEARBUSD": 0.07,
                    "AXSUSDT": 0.04,
                    "1INCHUSDT": 0.05,
                    "FLOWUSDT": 0.06,
                },
            },
        }

    sanity_check(strategy)
    title = title_strategy(strategy)
    file_path = "../store/results/"

    backtest = run_test(df, strategy)

    print("--------------------")
    print("> backtest complete")
    # print(backtest.head(40))
    chart_backtest(
        backtest, ["short_side", "long_side", "portfolio_value"], title=title
    )

    save_test = input("Would you like to export this test to csv? (y/n): ")

    subset = backtest.loc[:, ["short_side", "long_side", "portfolio_value"]]
    if save_test == "y":
        name = input("Enter the name of the strategy: ")
        subset.to_pickle(f"{file_path}tests/{name}.pkl")
        to_csv(subset, f"{file_path}csv/{name}")


def run_best_strategies():
    df = pd.read_pickle("../store/data/binance/portfolios_sample.pkl")

    df = df.iloc[:5]

    for idx, row in df.iterrows():
        long_weights = [round(x * 1000) / 1000 for x in row[2:4]]
        short_weights = [round(x * 1000) / 1000 for x in row[4:]]
        strategy = make_strategy_with_weights(long_weights, short_weights)
        perform_backtest(strategy=strategy)


# perform_backtest()
# sample_strategies()
# run_best_strategies()
