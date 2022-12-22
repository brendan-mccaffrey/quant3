def shape(df):
    """Get shape of dataframe"""
    num_rows = df.shape[0]
    num_cols = df.shape[1]
    print(f"The dataframe has {num_rows} rows and {num_cols} columns")


def num_rows(df):
    """Get rows of dataframe"""
    return df.shape[0]


def num_cols(df):
    """Get columns of dataframe"""
    return df.shape[1]
