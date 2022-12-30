import pickle
import pandas as pd

import dydx_api as dydxapi
import binance_api as binapi
import backtest as bt

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


def menu():
    print("| Options:")
    print("|")
    print("| [1] Pull new data from Binance")
    print("| [2] Pull new data from DyDx")
    print("| [3] Run backtest on data")
    print("| [4] Simulate backtests on binance data")
    print("| [5] Run top 5 backtests from simulation")
    print("| [6] Exit")
    print("|")
    return input("| > Enter your choice [1-6]: ")


def pull_binance_data():
    print("| Selected Option: [1] Pull new data from Binance")
    days = int(input("| > Enter number of days to pull data for: "))
    file_name = input("| > Enter file name to save data to: ")
    print("| Pulling new data from Binance...")
    binapi.create_data(tickers=binance_tickers, days=days, saveTo=file_name)


def main():
    print("-------------------------------------")
    print("| Welcome to the Quant3 Terminal")
    print("-------------------------------------")
    while True:
        match menu():
            case "1":
                pull_binance_data()
            case "2":
                print("| Pulling new data from DyDx...")

            case "3":
                print("| Running backtest on data...")

            case "4":
                print("| Selected Option: [4] Simulate backtests on binance data")
                file_name = input("| > Enter file name to load data from: ")
                df = pd.read_pickle("../store/data/binance/" + file_name + ".pkl")

                long_weights = []
                for ticker in binance_tickers[:2]:
                    weight = input("| > Enter weight for " + ticker + ": ")
                    long_weights.append(float(weight))
                short_weights = []
                for ticker in binance_tickers[2:]:
                    weight = input("| > Enter weight for " + ticker + ": ")
                    short_weights.append(float(weight))
                strategy = bt.make_strategy_with_weights(long_weights, short_weights)
                print("| Performing backtest...")
                bt.perform_backtest(df, strategy)

            case "5":
                print("| Running top 5 backtests from simulation...")

            case "6":
                print("| Exiting...")
                break

            case _:
                continue


main()
