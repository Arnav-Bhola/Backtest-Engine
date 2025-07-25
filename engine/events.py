class Event():
    def __init__(self, type):
        self.type = type

class MarketEvent(Event):
    def __init__(self, symbol):
        self.symbol = symbol
        super().__init__('MARKET')

class SignalEvent(Event):
    def __init__(self, symbol, action):
        super().__init__('SIGNAL')
        self.symbol = symbol
        self.action = action

class OrderEvent(Event):
    def __init__(self, symbol, action, quantity):
        super().__init__('ORDER')
        self.symbol = symbol
        self.action = action
        self.quantity = quantity


class FillEvent(Event):
    def __init__(self, symbol, action, quantity, price):
        super().__init__('FILL')
        self.symbol = symbol
        self.action = action
        self.quantity = quantity
        self.price = price