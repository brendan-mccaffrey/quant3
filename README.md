# Quant3

This is a little Python script that can be used to backtesting trading strategies on Binance or Dydx.

## Overview

- `main.py` - This is the main file that runs the execution terminal. Note only some of the functions are implemented in this terminal interface.
- `backtest.py` - This file contains the backtesting logic.
- `binance_api.py` - This file contains the Binance API logic for pulling and formatting data.
- `dydx_api.py` - This file contains the Dydx API logic for pulling and formatting data.


## Installation

Clone the repository and install the requirements:

```bash
pip install binance-python
pip install dydx3
pip install pandas
pip install numpy
pip install matplotlib
```

## Usage

Take a look through the code, and make changes to the following:

- `main.py` 
    - `binance_tickers` - Set the tickers you want to test here.
- `binance_api.py`
    - `binance_tickers` - Set the tickers you want to test here.
- `dydx_api.py`
    - `dydx_tickers` - Set the tickers you want to test here.
- `binance_strategy.json` - Set the strategy you want to test here.

Run the main execution terminal:

```bash
python3 main.py
```

## Example

This is a spread trade with the weights declared in the example `binance_strategy.json` file.
- Annualized Return: 110.20%
- Average Annualized Volatility: 29.30%
- Sharpe Ratio: 3.76
- Max 24hr Drawdown: -5.14%
- Max 1W Drawdown: -3.82%
- Previous 1M Performance: 11.29%
![](/store/results/charts/jan-2.png)

