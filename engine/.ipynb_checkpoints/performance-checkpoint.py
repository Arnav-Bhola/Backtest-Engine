import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Performance():
    def __init__(self, portfolio_history):
        self.portfolio_history = pd.DataFrame(portfolio_history)
        self.portfolio_history['datetime'] = pd.to_datetime(self.portfolio_history['datetime'])
        self.portfolio_history.set_index('datetime', inplace=True)
        self.total_return = 0.0
        self.max_drawdown = 0.0
        self.sharpe_ratio = 0.0

    def calculate_performance(self, risk_free_rate=0.05):
        self.portfolio_history['returns'] = self.portfolio_history['total_value'].pct_change().fillna(0)
        self.portfolio_history['equity_curve'] = (1 + self.portfolio_history['returns']).cumprod()
        self.equity_curve = self.portfolio_history['equity_curve']
        self.total_return = self.equity_curve.iloc[-1] - 1.0
        excess_returns = self.portfolio_history['returns'] - risk_free_rate
        self.sharpe_ratio = (
            np.sqrt(252) * excess_returns.mean() / excess_returns.std()
            if excess_returns.std() != 0 else 0
        )
        rolling_max = self.equity_curve.cummax()
        drawdown = self.equity_curve / rolling_max - 1.0
        self.max_drawdown = drawdown.min()

        return {
            'total_return': self.total_return,
            'sharpe_ratio': self.sharpe_ratio,
            'max_drawdown': self.max_drawdown,
        }
    
    def plot_equity_curve(self):
        if self.equity_curve is None or self.equity_curve.empty:
            raise ValueError("Equity curve is not calculated. Please run calculate_performance first.")

        sns.set_style("darkgrid")
        fig, ax = plt.subplots(figsize=(12, 6))

        sns.lineplot(x=self.equity_curve.index, y=self.equity_curve.values, color='royalblue', linewidth=2, ax=ax)

        ax.set_title("Equity Curve Over Time", fontsize=16)
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Equity (Cumulative Return)", fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()

        return fig

