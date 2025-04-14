from calculation import *
from accounting import *
from expense import *
from datetime import datetime
from plantuml import PlantUML
import subprocess
import pypandoc
import os

os.makedirs("out", exist_ok=True)

def generate_output(refunds: Calculation, team: List[Person], expenses: List[Expense]):
    #Generowanie diagramu w plantUML
    result = "@startuml\nleft to right direction\n"
    for person in team:
        result += f"object {person.name} {{\nNależność : {person.debt:.2f}zł\nWydatki: {person.expenses:.2f}zł\n}}\n"
    for accounting in refunds.accountings:
        result += f"{accounting.refund_giver.name} --> {accounting.refund_receiver.name} : {accounting.amount:.2f}zł\n"
    result += "@enduml\n"
    puml_file_path = "out/diagram_rozliczenie.puml"
    with open(puml_file_path, "w", encoding="utf-8") as diagram_file:
        diagram_file.write(result)
    plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
    plantuml.processes_file(puml_file_path)


    #Generowanie raportu w Markdown z eksportem do PDF
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

    result += "---\n### Indywidualny koszt\n|Osoba|Należność|\n|---|---|\n"
    for person in team:
        result += f"|{person.name}|{person.debt:.2f} zł|\n"

    result += "---\n### Rozliczenie"
    for accounting in refunds.accountings:
        result += f"\n\n{accounting.refund_giver.name} --- {accounting.amount:.2f} zł ---> {accounting.refund_receiver.name}\n"
    result += '\n\n---\n### Diagram rozliczenia\n'
    result += '<p align="center"><img src="diagram_rozliczenie.png" width="600"/></p>\n'
    result += f"\n*Raport wygenerowano: {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}*"
    subprocess.run(["markdown-pdf", "out/raport.md", "-o", "out/raport.pdf"])

    """
    with open("out/raport.md", "w", encoding="utf-8") as raport:
        raport.write(result)
    pypandoc.convert_file("out/raport.md", to="pdf", format="md", outputfile="out/raport.pdf", extra_args=["-t", "latex"])
    """