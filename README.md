# Simple Backtesting Engine

A lightweight, event-driven backtesting framework for simulating algorithmic trading strategies on historical financial data.

Built with modularity and clarity in mind, this engine allows users to implement and evaluate trading strategies with minimal setup. Currently includes a basic SMA crossover strategy, with plans for expansion.

## Features
- Event-driven architecture inspired by production trading systems.
- Modular design: easily extendable for new strategies, order types, and data sources.
- Performance analytics: visualize your equity curve, returns, and drawdown.
- SMA crossover strategy included for demonstration.

## Core Components

### Data Handler
- Fetches and manages historical market data using `yfinance`.
- Provides bar-by-bar data to the main loop.

### Strategy
- Currently implements a basic Simple Moving Average (SMA) crossover strategy.
- Can be extended to support more advanced indicators (e.g., RSI, MACD, ML-based models).

### Order Execution
- Simulates instant order execution.
- No slippage or commission costs (for now).

### Portfolio
Tracks:
- Cash balance
- Holdings
- Open/closed positions
- Portfolio value and PnL

### Events
Implements an event-driven system using custom events:
- **MarketEvent**: New market data is available.
- **SignalEvent**: Strategy generates a buy/sell/hold signal.
- **OrderEvent**: Order is placed.
- **FillEvent**: Order is executed.

### Performance
- Uses seaborn/matplotlib for equity curve visualization.
- Calculates:

    - Total return
    - Sharpe Ratio
    - Maximum drawdown

### Main Loop
- Drives the simulation by processing events in order.
- Updates the portfolio at each bar and logs portfolio snapshots for later analysis.

## Installation
```
git clone https://github.com/Arnav-Bhola/Backtest-Engine.git
cd Backtest-Engine
pip install -r requirements.txt
```
Required Dependencies:
- yfinance
- numpy
- pandas
- matplotlib
- seaborn

Usage: `main_backtest.ipynb` has all prewritten code for the sma crossover, run all cells of the jupyter notebook to see it working.

## Planned Updates
-  Add slippage and commission simulation
- Add stop-loss and take-profit functionality
- Implement more strategies (e.g., RSI, Bollinger Bands)
- Add multi-asset backtesting
- Add CSV and JSON reporting options
- Connect to Alpaca or Interactive Brokers for live/paper trading
- Add unit tests

## Why this Exists
This project started as a way to understand the internal mechanics of a backtesting engine from scratch. Unlike many off-the-shelf solutions, this is intentionally designed to be educational, hackable, and extendable; perfect for learning and experimentation.
