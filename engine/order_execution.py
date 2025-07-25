from engine.events import FillEvent

class SimulatedExecutionHandler():
    def __init__(self, portfolio):
        self.event_queue = portfolio.event_queue
        self.current_prices = portfolio.current_prices

    def execute_order(self, order_event):
        """Simulate order execution."""
        symbol = order_event.symbol
        action = order_event.action
        quantity = order_event.quantity

        if symbol not in self.current_prices:
            print(f"Price for {symbol} not available.")
            return None

        price = self.current_prices[symbol]

        # Assuming instant fill market order

        fill_event = FillEvent(symbol, action, quantity, price)
        
        # Add fill event to the event queue
        self.event_queue.append(fill_event)
        
        print(f"Executed {action} order for {quantity} shares of {symbol} at ${price:.2f}")
        return fill_event