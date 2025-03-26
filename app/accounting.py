from person import Person

class Accounting:
    def __init__(self, refund_giver: Person, refund_receiver: Person, amount: float):
        self.refund_giver = refund_giver
        self.refund_receiver = refund_receiver
        self.amuont = amount
        refund_giver.balance += amount
        refund_receiver.balance -= amount