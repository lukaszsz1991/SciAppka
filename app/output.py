from calculation import *
from accounting import *
from expense import *
from datetime import datetime
from plantuml import PlantUML
import subprocess
import time
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


    #Generowanie raportu w Markdown
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
    with open("out/raport.md", "w", encoding="utf-8") as raport:
        raport.write(result)

    #Generowanie .tex
    result = "\documentclass{report}\n\\usepackage[polish]{babel}\n\\usepackage[utf8]{inputenc}\n\\usepackage{graphicx}\n\\usepackage[T1]{fontenc}\n\\usepackage[left=3cm,right=3cm,top=3cm,bottom=3cm]{geometry}\n\\begin{document}\n\section*{Rozliczenie wydatków grupowych}\n\subsection*{Uczestnicy rozliczenia}\n\\begin{itemize}\n"
    for person in team:
        result += f"\item {person.name}\n"
    result += "\end{itemize}\n\subsection*{Wydatki}\n"
    for expense in expenses:
        result += f"\subsubsection*{{{expense.name}}}\n\\textbf{{Płacący: }} {expense.payer.name}\n\\textbf{{Kwota: }} {expense.amount:.2f}zł\n\\textbf{{Beneficjenci wydatku: }}{', '.join([person.name for person in expense.beneficiaries])}  \n \\textbf{{Należność na głowę: }} {expense.debt:.2f}zł\n"
    result += "\subsection*{Indywidualny koszt}\n"
    for person in team:
        result += f"{person.name} ---> {person.debt:.2f}zł\\\\"
    result += "\subsection*{Rozliczenie}\n"
    for accounting in refunds.accountings:
        result += f"{accounting.refund_giver.name} ---{accounting.amount:.2f}zł---> {accounting.refund_receiver.name}\\\\"
    result += "\subsection*{Diagram rozliczeniowy}\n\includegraphics[scale=0.4]{out/diagram_rozliczenie.png}\\\\\\end{document}"
    with open("out/raport.tex", "w", encoding="utf-8") as raporttex:
        raporttex.write(result)

    # Kompilacja LaTeX do PDF
    try:
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory=out", "out/raport.tex"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("✅ Plik PDF został wygenerowany w folderze 'out'.")
        print(result.stdout)  # (opcjonalnie: pokazuje wynik kompilacji)
    except subprocess.CalledProcessError as e:
        print("❌ Błąd kompilacji LaTeX:")
        print(e.stdout)
        print(e.stderr)
    except FileNotFoundError:
        print("❌ Nie znaleziono komendy 'pdflatex'. Upewnij się, że LaTeX jest zainstalowany i dodany do PATH.")