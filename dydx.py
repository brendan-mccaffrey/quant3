from dydx3 import Client
from web3 import Web3
import pandas as pd
import utils

mymarkets = [
    "ETH-USD",
    "1INCH-USD",
    "AVAX-USD",
    "CRV-USD",
    "UNI-USD",
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

    df.to_pickle("data/dydx/markets.pkl")


def get_funding(cl, days=200):
    """Get historical funding rates from dydx"""

    for market in mymarkets:
        long_df = pd.DataFrame()
        last_time = None
        for i in range(int(days / 4)):
            print("Getting funding for " + market + " " + str(i) + "/100")
            funding = cl.public.get_historical_funding(market, last_time)
            temp_df = pd.DataFrame.from_dict(funding.data)

            # format
            df = pd.DataFrame()
            for i in range(utils.num_rows(temp_df)):
                row = pd.DataFrame(temp_df.iloc[i].values[0], index=[i])
                df = pd.concat([df, row], axis=0)
            df.set_index("effectiveAt", inplace=True)

            # save last time for next call , python said this was a float?
            last_time = df.index[99]
            long_df = pd.concat([long_df, df], axis=0)

        long_df = long_df.drop_duplicates()
        print("\nFinished getting funding for " + market)

        # save to pickle
        long_df.to_pickle(f"data/dydx/funding/{market}.pkl")

    return


def main():
    cl = Client("https://api.dydx.exchange")
    get_markets(cl)
    # get_funding(cl)


main()
