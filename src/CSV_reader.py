import csv
import json
import os

from dotenv import load_dotenv

load_dotenv()


def CSV_reader(path_to_CSV=os.getenv("PATH_TO_CSV")):
    """Функция, считывающая данные из CSV-файла"""
    transactions = []
    with open(path_to_CSV, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        for row in reader:
            transactions.append(row)
    return transactions


transactions = CSV_reader()


def CSV_to_json(transactions,path=os.getenv("PATH_TO_TRANSACTIONS_JSON")):
    """Функция, записывающая данные из CSV-файла в формат json"""
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(transactions, json_file, ensure_ascii=False, indent=4)
