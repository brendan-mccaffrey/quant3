import time
import dateparser
import pytz
import json
import pandas as pd

from datetime import datetime, timedelta
from binance.client import Client

data_path = "../store/data/binance/"


def date_to_milliseconds(d):
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds
    :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    :return:
         None if unit not one of m, h, d or w
         None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    seconds_per_unit = {"m": 60, "h": 60 * 60, "d": 24 * 60 * 60, "w": 7 * 24 * 60 * 60}

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms


def get_historical_klines(symbol, interval, start_days_ago, end_str=None):
    """Get Historical Klines from Binance
    See dateparse docs for valid start and end string formats http://dateparser.readthedocs.io/en/latest/
    If using offset strings for dates add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    :param symbol: Name of symbol pair e.g BNBBTC
    :type symbol: str
    :param interval: Biannce Kline interval
    :type interval: str
    :param start_str: Start date string in UTC format
    :type start_str: str
    :param end_str: optional - end date string in UTC format
    :type end_str: str
    :return: list of OHLCV values
    """
    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 500

    # convert interval to useful value in seconds
    timeframe = interval_to_milliseconds(interval)

    # convert our date strings to milliseconds
    d = datetime.now() - timedelta(days=start_days_ago)
    start_ts = date_to_milliseconds(d)

    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        # fetch the klines from start_ts up to max 500 entries or the end_ts if set
        temp_data = client.get_klines(
            symbol=symbol,
            interval=interval,
            limit=limit,
            startTime=start_ts,
            endTime=end_ts,
        )

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0] + timeframe
        else:
            # it wasn't listed yet, increment our start date
            start_ts += timeframe

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data


def get_historical_data(
    symbol, interval=Client.KLINE_INTERVAL_1HOUR, start_days_ago=200, end=None
):
    data = get_historical_klines(symbol, interval, start_days_ago)
    df = pd.DataFrame(data)

    # format
    col_names = [
        "time",
        symbol + " price",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_asset_volume",
        "number_of_trades",
        "taker_buy_base_asset_volume",
        "taker_buy_quote_asset_volume",
        "ignore",
    ]
    rename_cols = {}
    for i in range(len(df.columns)):
        rename_cols[df.columns[i]] = col_names[i]
    df.rename(
        columns=rename_cols,
        inplace=True,
    )
    df.drop(
        columns=[
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base_asset_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ],
        axis=1,
        inplace=True,
    )
    df.set_index("time", inplace=True)
    df.index = pd.to_datetime(df.index, unit="ms")

    print(df.head(10))
    df.to_pickle(data_path + "price-history/" + symbol + ".pkl")


def get_historical_funding(symbol, start_days_ago=200, end_str=None):
    # create the Binance client, no need for api key
    client = Client("", "")

    # init our list
    output_data = []

    # setup the max limit
    limit = 1000

    # convert our date strings to milliseconds
    d = datetime.now() - timedelta(days=start_days_ago)
    start_ts = date_to_milliseconds(d)

    # if an end time was passed convert it
    end_ts = None
    if end_str:
        end_ts = date_to_milliseconds(end_str)

    idx = 0
    # it can be difficult to know when a symbol was listed on Binance so allow start time to be before list date
    symbol_existed = False
    while True:
        temp_data = client.get_funding_rate_history(symbol, start_ts, end_ts, limit)

        # handle the case where our start date is before the symbol pair listed on Binance
        if not symbol_existed and len(temp_data):
            symbol_existed = True

        if symbol_existed:
            # append this loops data to our output data
            output_data += temp_data

            # update our start timestamp using the last value in the array and add the interval timeframe
            start_ts = temp_data[len(temp_data) - 1][0]
        else:
            # it wasn't listed yet, increment our start date 5 days
            start_ts += timedelta(days=5).total_seconds() * 1000

        idx += 1
        # check if we received less than the required limit and exit the loop
        if len(temp_data) < limit:
            # exit the while loop
            break

        # sleep after every 3rd call to be kind to the API
        if idx % 3 == 0:
            time.sleep(1)

    return output_data


def main():
    # binance does not have YGG, MC, FXS
    # AXS, CRV, HNT, DYDX, FLOW, 1INCH only USDT pair

    resp = get_historical_funding("BTCBUSD", start_days_ago=1)
    df = pd.DataFrame(resp)
    print(df.head)
    return

    tickers = [
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

    for ticker in tickers:
        # get_historical_data(ticker)
        get_historical_funding(ticker)


main()
