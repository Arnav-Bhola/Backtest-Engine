import yfinance as yf

class DataHandler():
    def __init__(self, ticker):
        self.ticker = ticker
        self.current_index = None
        self.data = None

    def fetch_data(self, period='max'):
        """Fetch historical data for the given ticker."""
        dat = yf.Ticker(self.ticker)
        unfiltered_data = dat.history(period=period)
        filtered_data=unfiltered_data[['Close']]
        self.data=filtered_data
        return filtered_data

    def get_data(self):
        """Return the fetched data."""
        if self.data is not None:
            return self.data
        else:
            raise ValueError("Data not fetched yet. Call fetch_data() first.")
        
    def get_sma(self, window):
        """Calculate and return the Simple Moving Average (SMA) for the data."""
        if self.data is None:
            raise ValueError("Data not fetched yet. Call fetch_data() first.")
        self.data['SMA_{}'.format(window)] = self.data['Close'].rolling(window=window).mean()
        return self.data['SMA_{}'.format(window)]
    
    def get_next_bar(self):
        """Get the next bar of data."""
        if self.data is None:
            raise ValueError("Data not fetched yet. Call fetch_data() first.")
        if self.current_index is None or self.current_index >= len(self.data):
            raise IndexError("No more data available.")
        next_bar = self.data.iloc[self.current_index]
        self.current_index += 1
        return next_bar
    
    def prepare(self, fast_window, slow_window):
        self.get_sma(fast_window)
        self.get_sma(slow_window)
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.current_index = max(fast_window, slow_window)

    def reset(self):
        """Reset the current index to the beginning of the data."""
        if self.fast_window is not None and self.slow_window is not None:
            self.current_index = max(self.fast_window, self.slow_window)
        else:
            raise ValueError("Windows not set yet. Call prepare() first.")

if __name__ == "__main__":
    dataHandler = DataHandler("AAPL")
    dataHandler.fetch_data()
    dataHandler.prepare(fast_window=10, slow_window=30)
    while True:
        try:
            next_bar = dataHandler.get_next_bar()
            print(next_bar)
        except IndexError:
            print("No more data available.")
            break