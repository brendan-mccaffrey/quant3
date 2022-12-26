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

shorts = mymarkets[1:]
long = "ETH-USD"

df = pd.read_pickle("../data/dydx/funding/combined.pkl")
first = df.iloc[0]


def compute_value_equal_short(row):
    """Compute value of equal weight short strategy"""

    print(shorts)
    # print(row.name, " | ", row)

    weight_per_item = 1 / (len(mymarkets) - 1)
    if row.name == first.name:
        print("First row, skipping...")
    else:
        prev = df.loc[row.name - pd.Timedelta(hours=1)]

        short_day_factor = 0
        for short in shorts:
            # hr change = (today - yesterday) / yesterday
            hr_change = (row[short + " price"] - float(prev[short + " price"])) / float(
                prev[short + " price"]
            )
            # negate change and factor funding
            hr_short_perf = -hr_change * (1 + row[short + " rate"])
            short_day_factor += (1 + hr_short_perf) * weight_per_item

        row["shorts_value"] = prev["shorts_value"] * short_day_factor

        eth_hr_change = (row[long + " price"] - float(prev[long + " price"])) / float(
            prev[long + " price"]
        )
        eth_hr_perf = eth_hr_change * (1 - row[long + " rate"])
        row["longs_value"] = prev["longs_value"] * eth_hr_perf

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

    df = pd.read_pickle("../data/dydx/funding/combined.pkl")

    # add a new column of 0s to the dataframe
    df["shorts_value"] = 500000
    df["longs_value"] = 500000

    print(df.head(3))

    df = df.astype(float)

    df.iloc[:3].apply(compute_value_equal_short, axis=1)

    print(df.head(3))

    # hello

    # print(df.head())

    # print(df["shorts_value"])

    # df["shorts_value"] = df.apply(compute_value_equal_short, axis=1)

    # df["shorts_value"] = df["shorts_value"].shift(1) * df["1INCH-USD price"]

    # print(df.head())


backtest_equal_short()
