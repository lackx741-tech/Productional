import uuid


class SmartWallet:
    def __init__(self):
        self.address = str(uuid.uuid4())
        self.balance = 0.0

    def credit(self, amount: float):
        self.balance += amount

    def debit(self, amount: float):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
