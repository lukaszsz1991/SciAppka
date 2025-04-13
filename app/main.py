from person import Person
from expense import Expense
from calculation import Calculation
from output import *

print("Program rozlicza wydatki grupowe i na koniec podaje, kto komu ile ma zwrócić.")
names = input("\nPodaj imiona (unikatowe) uczesników rozliczenia (rozdzielone przecinkami):\n")
team = []
for name in names.split(","):
    team.append(Person(name.strip()))
expenses = []
choice = 1

def add_expense():
    expense_name = input("Podaj nazwę wydatku:\n")
    print("Kto zapłacił(podaj numer odpowiedniej osoby)")
    for person in team:
        print(f"{team.index(person) + 1} - {person.name}")
    payer = int(input()) - 1
    amount = float(input(f"Jaką kwotę zapłacił {team[payer].name}?\n"))
    print("Wybierz, kto korzystał z tego wydatku: (podaj numery rozdzielone przecinkami)")
    for person in team:
        print(f"{team.index(person) + 1} - {person.name}")
    print(f"{len(team) + 1} - wszyscy")
    beneficiaries_numbers = list(map(int, input("Podaj liczby oddzielone przecinkami: ").split(",")))
    beneficiaries = []
    if beneficiaries_numbers[0] == len(team) + 1:
        beneficiaries = team
    else:
        for person in beneficiaries_numbers:
            beneficiaries.append(team[person - 1])
    expenses.append(Expense(expense_name, team[payer], amount, beneficiaries))

while choice != 2:
    add_expense()
    choice = int(input("\n1 - dodaj wydatek\n2 - rozliczenie"))

for person in team:
    print(person)

refunds = Calculation(team)
generate_diagram(refunds)
generate_md(team, expenses, refunds)
print(refunds)
