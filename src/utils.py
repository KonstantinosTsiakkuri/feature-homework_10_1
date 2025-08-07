import json
import os

from dotenv import load_dotenv

load_dotenv()


def function(path=os.getenv("PATH_TO_JSON")):
    """Функция принимает .json-файл и возвращает список транзакций """
    if path:
        with open(path, encoding="utf-8") as json_file:
            operations_list = json.load(json_file)
        return operations_list
    if not path or list not in path:
        return []
