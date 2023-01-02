from dydx3 import Client
from web3 import Web3
import pandas as pd
import utils

data_path = "./store/data/dydx/"
dydx_markets = [
    "ETH-USD",
    "1INCH-USD",
    "AVAX-USD",
    "CRV-USD",
    "UNI-USD",
    "NEAR-USD",
    "COMP-USD",
]


def get_markets_list(cl, mymarkets=dydx_markets, saveTo=None):
    """Retreive all markets from dydx"""

    markets = cl.public.get_markets()
    df = pd.DataFrame.from_dict(markets.data)

    # parse out only my markets
    df = df.loc[mymarkets]

    # format
    new_df = pd.DataFrame()
    for i in range(utils.num_rows(df)):
        row = pd.DataFrame(df.iloc[i].values[0], index=[i])
        new_df = pd.concat([new_df, row], axis=0)
    new_df.set_index("market", inplace=True)

    # # move eth to top
    # eth = new_df.loc["ETH-USD"]
    # new_df = new_df.drop("ETH-USD")
    # new_df = pd.DataFrame(eth).T.append(new_df)

    # save
    if saveTo:
        new_df.to_pickle(data_path + f"{saveTo}.pkl")


def get_historical_data(cl, mymarkets=dydx_markets, days=200, save=False):
    """Get historical prices & funding rates from dydx"""

    for market in mymarkets:
        df = pd.DataFrame()
        last_time = None
        for i in range(int(days / 4)):
            print("Pulling " + market + " " + str(i) + "/" + str(days / 4))
            resp = cl.public.get_historical_funding(market, last_time)
            data_df = pd.DataFrame.from_dict(resp.data)

            # format
            temp_df = pd.DataFrame()
            for i in range(utils.num_rows(data_df)):
                row = pd.DataFrame(data_df.iloc[i].values[0], index=[i])
                temp_df = pd.concat([temp_df, row], axis=0)
            temp_df.set_index("effectiveAt", inplace=True)

            # save last time for next call , python said this was a float?
            last_time = temp_df.index[99]
            df = pd.concat([df, temp_df], axis=0)
        df = df.drop_duplicates()

        # save
        if save:
            df.to_pickle(data_path + f"{market}.pkl")
            print("Saved " + market + " to pickle")
        print("Market: ", market)
        print(df.head(4))


def combine_market_dfs(mymarkets=dydx_markets, saveTo=None):
    """Combine all dataframes into one master dataframe"""

    # combine
    df = pd.DataFrame()
    for market in mymarkets:
        temp_df = pd.read_pickle(data_path + market + ".pkl")
        temp_df.rename(
            columns={"rate": market + " rate", "price": market + " price"},
            inplace=True,
        )
        temp_df.drop(columns=["market"], inplace=True)
        df = pd.concat([df, temp_df], axis=1, join="outer")

    # format
    df.fillna(0, inplace=True)
    df.index = pd.to_datetime(df.index)
    df.sort_index(axis=0, inplace=True)

    # save
    if saveTo:
        df.to_pickle(data_path + f"{saveTo}.pkl")
        print("Saved " + f"{saveTo}.pkl")

    print("Combined Dataframe")
    print(df.head(4))


def get_data(name="dydx_data"):
    cl = Client("https://api.dydx.exchange")

    get_markets_list(cl)
    get_historical_data(cl, dydx_markets, days=200)
    combine_market_dfs(dydx_markets, saveTo=name)
