from calculation import *
from accounting import *
from expense import *
import pypandoc
import os

os.makedirs("out", exist_ok=True)

def generate_diagram(calculation):
    result = "@startuml\n"
    for accounting in calculation.accountings:
        result += f"{accounting.refund_giver.name} --> {accounting.refund_receiver.name} : {accounting.amount}\n"
    result += "@enduml\n"
    with open("out/diagram_rozliczenie.puml", "w", encoding="utf-8") as diagram_file:
        diagram_file.write(result)

def generate_md(team: List[Person], expenses: List[Expense], refunds: Calculation):
    result = "# Raport rozliczeniowy wydatków grupowych\n\n"

    result += "\n### Uczestnicy rozliczenia\n"
    for person in team:
        result += f"- {person.name}\n"
    result += "\n"

    result += "---\n### Wydatki\n"
    for expense in expenses:
        result += f"#### {expense.name}\n"
        result += f"**Płacący:** {expense.payer.name}  \n"
        result += f"**Kwota:** {expense.amount:.2f} zł  \n"
        result += f"**Beneficjenci wydatku:** {', '.join([person.name for person in expense.beneficiaries])}  \n"
        result += f"**Należność na głowę:** {expense.debt:.2f} zł\n\n"

    result += "---\n### Indywidualny koszt wyprawy\n|Osoba|Należność|\n|---|---|\n"
    for person in team:
        result += f"|{person.name}|{person.debt:.2f} zł|\n"

    result += "---\n### Rozliczenie"
    for accounting in refunds.accountings:
        result += f"\n\n{accounting.refund_giver.name} --- {accounting.amount:.2f} zł ---> {accounting.refund_receiver.name}\n"

    with open("out/raport.md", "w", encoding="utf-8") as raport:
        raport.write(result)
    pypandoc.convert_file("out/raport.md", to="pdf", format="md", outputfile="out/raport.pdf", extra_args=["-t", "latex"])
