from dydx3 import Client
from web3 import Web3
import pandas as pd
import pickle

dydx_client = Client("https://api.dydx.exchange")

markets = dydx_client.public.get_markets()

# markets.sort(key=lambda x: x["name"])

df = pd.DataFrame.from_dict(markets.data)

print(df.head(5))
