from dydx3 import Client
from web3 import Web3
import pandas as pd
import pickle
import utils
from datetime import datetime

mymarkets = [
    "1INCH-USD",
    "AVAX-USD",
    "CRV-USD",
    "UNI-USD",
    "ETH-USD",
    "NEAR-USD",
    "COMP-USD",
]


def get_markets(cl):
    """Get markets from dydx"""
    markets = cl.public.get_markets()
    df = pd.DataFrame.from_dict(markets.data)
    df = df.loc[mymarkets]

    # format
    new_df = pd.DataFrame()
    for i in range(utils.num_rows(df)):
        row = pd.DataFrame(df.iloc[i].values[0], index=[i])
        # new_df = new_df.append(row)
        new_df = pd.concat([new_df, row], axis=0)
    new_df.set_index("market", inplace=True)

    # move eth to top
    eth = new_df.loc["ETH-USD"]
    new_df = new_df.drop("ETH-USD")
    new_df = pd.DataFrame(eth).T.append(new_df)

    return new_df


def get_funding(cl):
    """Get funding rates from dydx"""

    funding = cl.public.get_historical_funding(mymarkets[0])
    df = pd.DataFrame.from_dict(funding.data)

    # format
    new_df = pd.DataFrame()
    for i in range(utils.num_rows(df)):
        row = pd.DataFrame(df.iloc[i].values[0], index=[i])
        new_df = pd.concat([new_df, row], axis=0)
    new_df.set_index("effectiveAt", inplace=True)

    print("Tail of first call")
    print(new_df.tail())

    # print("HERE")
    # print(new_df.iloc[99])
    # last_time = datetime.fromisoformat(str(new_df.index[99]))
    # print("Converted")
    # print(last_time)

    # # get the last row
    # last_row = new_df.iloc[-1]

    # # get the index of the last row
    # last_row_index = new_df.index[-1]
    # print(f"Last row of first call: {last_row_index} {last_row.values}")

    next_funding = cl.public.get_historical_funding(mymarkets[0], new_df.index[99])
    df = pd.DataFrame.from_dict(next_funding.data)
    new_df2 = pd.DataFrame()
    for i in range(utils.num_rows(df)):
        row = pd.DataFrame(df.iloc[i].values[0], index=[i])
        new_df2 = pd.concat([new_df2, row], axis=0)
    new_df2.set_index("effectiveAt", inplace=True)
    print("head of second call")
    print(new_df2.head())
    # utils.shape(df)

    # print(df.iloc[0].values[0])
    # print(df.iloc[1].values[0])
    # print(df.iloc[99].values[0])

    # print(df.head())
    return
    df = df.loc[mymarkets]

    # format
    new_df = pd.DataFrame()
    for i in range(utils.num_rows(df)):
        row = pd.DataFrame(df.iloc[i].values[0], index=[i])
        new_df = new_df.append(row)
    new_df.set_index("market", inplace=True)

    # move eth to top
    eth = new_df.loc["ETH-USD"]
    new_df = new_df.drop("ETH-USD")
    new_df = pd.DataFrame(eth).T.append(new_df)

    return new_df


def update_markets(cl):
    """Update markets"""
    df = get_markets(cl)
    print("Retreived markets\n", df.head())
    print("Saving")
    df.to_pickle("data/markets2.pkl")


def main():
    cl = Client("https://api.dydx.exchange")

    # update_markets(cl)
    get_funding(cl)


main()
