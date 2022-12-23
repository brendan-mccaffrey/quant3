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


def sort_df():
    df = pd.read_pickle("data/dydx/funding/combined.pkl")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index(axis=0)
    df.to_pickle("data/dydx/funding/combined.pkl")


def make_master_df():
    """Make master df"""
    master_df = pd.DataFrame()
    for market in mymarkets:
        df = pd.read_pickle("data/dydx/funding/" + market + ".pkl")
        df.rename(
            columns={"rate": market + " rate", "price": market + " price"},
            inplace=True,
        )
        df.drop(columns=["market"], inplace=True)

        master_df = pd.concat([master_df, df], axis=1, join="outer")

    df = master_df
    df.fillna(0, inplace=True)

    df_sorted = df.sort_index(axis=0)

    # df.sort_index(axisascending=True, inplace=True)
    print(df_sorted.head())

    # df.to_pickle("data/dydx/funding/combined.pkl")

    # # 96 rows with null values, COMP, 1INCH, NEAR, CRV, mostly COMP
    # null_mask = df.isnull()
    # null_rows = null_mask.sum(axis=1)
    # for index, row in null_rows.iteritems():
    #     if row > 0:
    #         print(index, ":", df.loc[index])
    # print("Total Null rows: " + str(null_rows.sum()))

    # print(index, ":", row)
    # print(i)
    # print(df.iloc[i])

    # .sum()
    # print(null_row_count)

    # print(master_df.isnull().any(axis=1)).sum()

    # # Select rows that contain null values
    # null_rows = df[null_mask]
    # print(null_rows)

    # # Select columns that contain null values
    # null_columns = df.loc[:, null_mask.any()]
    # print(null_columns)

    # # Select individual cells that contain null values
    # null_cells = df.loc[null_mask]
    # print(null_cells)

    # if master_df.isnull().any(axis=1).any():
    #     print("DataFrame contains null values in at least one row")
    # if master_df.isnull().any(axis=0).any():
    #     print("DataFrame contains null values in at least one column")

    # null_mask = master_df.isnull()
    # print(null_mask)
    # null_loc = master_df.loc[null_mask]
    # print(null_loc)

    # print(master_df)


sort_df()
# # master_df.to_pickle("data/dydx/funding/master.pkl")
# return master_df
