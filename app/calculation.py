from person import Person
from typing import List
from accounting import Accounting

class Calculation:
    def __init__(self, team: List[Person]):
        self.team = team
        self.accountings = []
        for refund_giver in team:
            if refund_giver.balance < 0:
                for refund_receiver in team:
                    if refund_receiver.balance > 0:
                        if abs(refund_giver.balance) > refund_receiver.balance:
                            self.accountings.append(Accounting(refund_giver, refund_receiver, refund_receiver.balance))
                        else:
                            self.accountings.append(Accounting(refund_giver, refund_receiver, abs(refund_giver.balance)))
                    if refund_giver.balance == 0:
                        break

    def __str__(self):
        parts = []
        for refund in self.accountings:
            parts.append(f"{refund.refund_giver.name} ma zawrócić {refund.amuont:.2f}zł -> {refund.refund_receiver.name}")
        return "\n"+"\n".join(parts)