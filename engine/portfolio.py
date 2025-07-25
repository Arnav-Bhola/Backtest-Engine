from engine.events import OrderEvent

class Portfolio():
    def __init__(self, initial_balance=100000):
        self.initial_cash = initial_balance
        self.cash = initial_balance
        self.total_value= initial_balance
        self.positions = {}
        self.holdings = {}
        self.current_prices={}
        self.cost_basis = {}
        self.realized_pnl=0.0
        self.unrealized_pnl=0.0
        self.total_pnl = self.unrealized_pnl + self.realized_pnl
        self.event_queue=[]

    def update_price(self, symbol, bar):
        """Update the current price of a symbol."""
        self.current_prices[symbol] = bar['Close']

    def process_signal(self, signal_event):
        """Process a signal event and update positions."""
        symbol = signal_event.symbol
        action = signal_event.action

        self.order_size = 1  # Default order size, can be calculated based on strategy

        if action == "Buy":
            if self.cash >= self.current_prices[symbol] * self.order_size:
                return OrderEvent(symbol, action, self.order_size)
        elif action == "Sell":
            if symbol in self.positions and self.positions[symbol] >= self.order_size:
                return OrderEvent(symbol, action, self.order_size)
        else:
            return None
    
    def process_fill(self, fill_event):
        """Process a fill event and update portfolio."""
        symbol = fill_event.symbol
        action = fill_event.action
        quantity = fill_event.quantity
        price = fill_event.price

        if action == "Buy":
            prev_quantity = self.positions.get(symbol, 0)
            prev_price = self.cost_basis.get(symbol, 0)
            new_quantity = prev_quantity + quantity

            new_cost_basis = (
                (prev_price * prev_quantity + price * quantity) / new_quantity
                if new_quantity > 0 else 0.0
            )

            self.positions[symbol] = new_quantity
            self.cost_basis[symbol] = new_cost_basis
            self.cash -= price * quantity
        
        elif action == "Sell":
            cost = self.cost_basis[symbol]
            pnl = (price - cost) * quantity
            self.realized_pnl += pnl

            self.positions[symbol] -= quantity
            if self.positions[symbol] == 0:
                del self.positions[symbol]
                del self.cost_basis[symbol]

            self.cash += price * quantity

    def update_total_value(self):
        """Update the total value of the portfolio."""
        self.total_value = self.cash
        self.unrealized_pnl = 0.0

        for symbol, quantity in self.positions.items():
            if symbol in self.current_prices:
                market_price = self.current_prices[symbol]
                market_value = quantity * market_price
                self.total_value += market_value
                self.holdings[symbol] = market_value

                cost = self.cost_basis.get(symbol, 0.0)
                self.unrealized_pnl += (market_price - cost) * quantity

        self.total_pnl = self.realized_pnl + self.unrealized_pnl

    def print_summary(self):
        """Print the summary of the portfolio."""
        print(f"Total Cash: ${self.cash:.2f}")
        print(f"Total Value: ${self.total_value:.2f}")
        print(f"Total PnL: ${self.total_pnl:.2f}")
        print("Positions:")
        for symbol, quantity in self.positions.items():
            print(f"{symbol}: {quantity} shares")
        print("Holdings:")
        for symbol, value in self.holdings.items():
            print(f"{symbol}: ${value:.2f}")