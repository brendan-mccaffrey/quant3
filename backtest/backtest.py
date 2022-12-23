import pandas as pd

mymarkets = [
    "ETH-USD",
    "1INCH-USD",
    "AVAX-USD",
    "CRV-USD",
    "UNI-USD",
    "NEAR-USD",
    "COMP-USD",
]

df = pd.read_pickle("data/dydx/funding/combined.pkl")

first = df.iloc[0]


def compute_value_equal_short(row):
    """Compute value of equal weight short strategy"""

    weight_per_item = 1 / (len(mymarkets) - 1)
    if row.name == first.name:
        value = 500000
    else:
        # get previous row value
        prev = row.name - pd.Timedelta(hours=1)
        print(df.loc[prev])
        print()
        # value = df.loc[prev]["shorts_value"] * 0
        # if df.loc[prev] == 0:
        #     print("AH")

    # print("They are equal?", row.name == first.name)

    # for market in mymarkets:
    #     value += row[market + " price"] * row[market + " rate"]
    # return value


def backtest_equal_short(total_size=1e7, start_date="2022-08-01"):
    """Backtest equal weight short strategy"""

    df = pd.read_pickle("data/dydx/funding/combined.pkl")

    # add a new column of 0s to the dataframe
    df["shorts_value"] = 500000

    print(df.head())

    df.iloc[:5].apply(compute_value_equal_short, axis=1)

    # hello

    # print(df.head())

    # print(df["shorts_value"])

    # df["shorts_value"] = df.apply(compute_value_equal_short, axis=1)

    # df["shorts_value"] = df["shorts_value"].shift(1) * df["1INCH-USD price"]

    # print(df.head())


backtest_equal_short()
