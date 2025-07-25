from engine.data_handler import DataHandler

class Strategy():
    def __init__(self, threshold, fast_window, slow_window):
        self.upper_threshold = 1 + threshold / 100
        self.lower_threshold = 1 - threshold / 100
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.previous_day = None

    def verdict(self, bar):
        fast_sma = bar[f'SMA_{self.fast_window}']
        slow_sma = bar[f'SMA_{self.slow_window}']
        above = fast_sma > slow_sma * self.upper_threshold
        below = fast_sma < slow_sma * self.lower_threshold

        if self.previous_day is None:
            if above:
                self.previous_day = "Above"
            elif below:
                self.previous_day = "Below"
            else:
                self.previous_day = None
            return "Hold"

        if self.previous_day == "Above":
            if below:
                self.previous_day = "Below"
                return "Sell"
            elif above:
                self.previous_day = "Above"
            else:
                self.previous_day = None
            return "Hold"

        if self.previous_day == "Below":
            if above:
                self.previous_day = "Above"
                return "Buy"
            elif below:
                self.previous_day = "Below"
            else:
                self.previous_day = None
            return "Hold"
        
        return "Hold"

if __name__ == "__main__":
    ticker = "AAPL"
    fast_window = 10
    slow_window = 30
    threshold = 0.1

    # Initialize DataHandler and fetch data
    data_handler = DataHandler(ticker)
    data_handler.fetch_data()
    data_handler.prepare(fast_window, slow_window)

    # Initialize Strategy
    strategy = Strategy(threshold, fast_window, slow_window)

    # Test on few bars
    for i in range(10000):
        try:
            bar = data_handler.get_next_bar()
            if i > 9500:
                action = strategy.verdict(bar)
                print(f"Date: {bar.name.date()}, Close: {bar['Close']:.2f}, SMA: {bar['SMA_{}'.format(fast_window)]:.2f},  SMA: {bar['SMA_{}'.format(slow_window)]:.2f}, Action: {action}")
        except IndexError:
            print("No more data available.")
            break
