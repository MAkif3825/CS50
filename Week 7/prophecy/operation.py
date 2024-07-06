import csv
from cs50 import SQL

list = []
with open("students.csv") as file:
    reader = csv.DictReader(file)
    for element in reader:
        list.append(element)

db = SQL("sqlite:///roster.db")

for i in range(len(list)):
    db.execute("INSERT  INTO studentss (id, student_name) VALUES (?,?)", list[i]["id"], list[i]["student_name"])
    db.execute("INSERT  INTO assignments (student_id, house_name) VALUES (?,?)", list[i]["id"], list[i]["house"])