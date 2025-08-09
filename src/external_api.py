import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def transaction_function():
    """Функция возвращает информацию о транзакции и конвертирует валюту в рубли"""
    path = os.getenv("PATH_TO_JSON")
    with open(path, encoding="utf-8") as json_file:
        operations_list = json.load(json_file)
    for transaction in operations_list:
        if "currency" in transaction["operationAmount"] and "name" in transaction["operationAmount"]["currency"]:
            if transaction["operationAmount"]["currency"]["name"] == "руб.":
                yield f"{float(transaction["operationAmount"]["amount"])} руб"
            elif (
                transaction["operationAmount"]["currency"]["name"] == "USD"
                or transaction["operationAmount"]["currency"]["name"] == "EUR"
            ):
                url = "https://api.apilayer.com/exchangerates_data/convert"
                headers = {"apikey": os.getenv("API_KEY")}
                if not headers["apikey"]:
                    raise ValueError("API_KEY not found in environment variables")
                payload = {
                    "amount": float(transaction["operationAmount"]["amount"]),
                    "from": transaction["operationAmount"]["currency"]["name"],
                    "to": "RUB",
                }
                response = requests.get(url, headers=headers, params=payload)
                status_code = response.status_code
                result = response.json()
                if status_code == 200:
                    print(status_code)
                    yield f"{result['result']} руб"
                else:
                    print(f"Запрос не был успешным. Возможная причина: {response.reason}")
        else:
            continue
