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
    print("| [3] Run backtest on Binance data")
    print("| [4] Run backtest on Binance data")
    print("| [5] Simulate backtests on binance data")
    print("| [6] Run top 5 backtests from simulation")
    print("| Any Other Input Will Exit")
    print("|")
    return input("| > Enter your choice [1-6]: ")


def pull_binance_data():
    print("| Selected Option: [1] Pull new data from Binance")
    days = int(input("| > Enter number of days to pull data for: "))
    file_name = input("| > Enter file name to save data to: ")
    print("| Pulling new data from Binance...")
    binapi.create_data(tickers=binance_tickers, days=days, saveTo=file_name)


def backtest_binance():
    print("| Selected Option: [4] Simulate backtests on binance data")
    file_name = input("| > Enter file name to load data from: ")
    df = pd.read_pickle("./store/data/binance/" + file_name + ".pkl")
    strategy = bt.load_strategy()
    choice = input("| Is this the correct strategy? [y/n]: ")
    if choice == "n":
        choice = input(
            "| Would you like to input a custom strategy in the terminal? [y/n]: "
        )
        if choice == "y":
            strategy = make_custom_strategy()
        else:
            return

    print("| Performing backtest...")
    bt.perform_backtest(df, strategy)


def make_custom_strategy():
    long_weights = []
    for ticker in binance_tickers[:2]:
        weight = input("| > Enter weight for " + ticker + ": ")
        long_weights.append(float(weight))
    short_weights = []
    for ticker in binance_tickers[2:]:
        weight = input("| > Enter weight for " + ticker + ": ")
        short_weights.append(float(weight))
    strategy = bt.make_strategy_with_weights(long_weights, short_weights)
    return strategy


def pull_dydx_data():
    print("| Pulling new data from DyDx...")
    file_name = input("| > Enter file name to save data to: ")
    dydxapi.get_data(name=file_name)


def backtest_dydx():
    print("| Running backtest on data...")
    # TODO
    print("| This is not yet implemented from the main menu.")
    print("|")
    print("| Please run the backtest from the backtest.py file.")
    print("| This may require some changes to the code.")


def simulate_backtests():
    print("| Simulating random binance strategies...")
    # TODO
    print("| This is not yet implemented from the main menu.")
    print("|")
    print("| Please run the backtest from the backtest.py file.")
    print("| This may require some changes to the code.")


def run_best_simulations():
    print("| Running top 5 backtests from simulation...")
    # TODO
    print("| This is not yet implemented from the main menu.")
    print("|")
    print("| Please run the backtest from the backtest.py file.")
    print("| This may require some changes to the code.")


def main():
    print("-------------------------------------")
    print("| Welcome to the Quant3 Terminal")
    print("-------------------------------------")
    while True:
        match menu():
            case "1":
                pull_binance_data()
            case "2":
                pull_dydx_data()
            case "3":
                backtest_dydx()
            case "4":
                backtest_binance()
            case "5":
                simulate_backtests()
            case "6":
                run_best_simulations()
            case _:
                print("| Exiting...")
                break


main()
