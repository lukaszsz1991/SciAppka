from person import Person
from expense import Expense
from calculation import Calculation
from output import *

useTestData = True
if not useTestData:
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
else: #Zestaw danych testowych
    team = []
    expenses = []
    team.append(Person("Maciek"))
    team.append(Person("Agata"))
    team.append(Person("Wojtek"))
    team.append(Person("Milena"))
    team.append(Person("Eugeniusz"))
    team.append(Person("Andrzej"))
    expenses.append(Expense("Zakupy spożywcze",payer=team[0], amount=120.00, beneficiaries=[team[0], team[1], team[2]]))
    expenses.append(Expense("Bilety do kina", payer=team[1], amount=90.00, beneficiaries=[team[0], team[1], team[2], team[3]]))
    expenses.append(Expense("Pizza", payer=team[2], amount=80.00, beneficiaries=team))
    expenses.append(Expense("Taxi", payer=team[4], amount=60.00, beneficiaries=[team[4], team[5]]))
    expenses.append(Expense("Hotel", payer=team[3], amount=200.00, beneficiaries=team))
    expenses.append(Expense("Dyskoteka", payer=team[1], amount=70.00, beneficiaries=[team[1], team[3]]))

refunds = Calculation(team)
generate_output(refunds, team, expenses)
print(refunds)
