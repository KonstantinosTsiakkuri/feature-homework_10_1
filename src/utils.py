import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(LOG_DIR / "utils.log", mode="w", encoding="utf-8")
logger.addHandler(file_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)


def function(path=os.getenv("PATH_TO_JSON")):
    """Функция принимает .json-файл и возвращает список транзакций"""
    if path:
        logger.info("Проверка корректности пути до файла")
        with open(path, encoding="utf-8") as json_file:
            operations_list = json.load(json_file)
        logger.info("Возврат списка транзакций")
        return operations_list
    if not path or list not in path:
        logger.info("Обработка некорректного вида файла")
        return []
