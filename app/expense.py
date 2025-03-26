from person import Person
from typing import List

class Expense:
    def __init__(self, name: str, payer: Person, amount: float, beneficiaries: List[Person]):
        self.name = name #Nazwa wydatku
        self.payer = payer #Płacący
        self.amount = amount
        self.beneficiaries = beneficiaries #Osoby, które powinny partycypować w kosztach danego wydatku
        self.payer.expenses += amount
        self.payer.balance += amount
        self.is_payer_beneficiary = False
        self.debt = amount / len(self.beneficiaries)
        for person in beneficiaries:
            person.debt += self.debt
            person.balance -= self.debt
            if person == self.payer:
                self.is_payer_beneficiary = True

    def __str__(self):
        # Tworzymy listę beneficjentów, z wyjątkiem płacącego
        other_beneficiaries = ", ".join(person.name for person in self.beneficiaries if person != self.payer)
        beneficiaries_to_string = "Beneficjentami"
        if self.is_payer_beneficiary:
            beneficiaries_to_string = "Pozostałymi beneficjentami"
        return f"\nWydatek: {self.name}\n{self.payer.name} zapłacił(a) {self.amount:.2f} zł.\n{beneficiaries_to_string} są {other_beneficiaries}.\nNależność na głowę wyniosła {self.debt:.2f} zł."