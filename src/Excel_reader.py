import json
import os

import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def excel_reader(path_to_excel=os.getenv("PATH_TO_EXCEL")):
    """Функция, считывающая данные из excel-файла"""
    df = pd.read_excel(path_to_excel)
    records = df.to_dict(orient="records")  # преобразуем в список словарей
    result = json.dumps(records, ensure_ascii=False, indent=4)
    return result
