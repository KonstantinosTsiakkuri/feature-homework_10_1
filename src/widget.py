import re
from typing import Dict, List, Union


def mask_account_card(number_type: str) -> Union[List[Dict], str]:
    """Функция принимает тип и номер карты или счета и возвращает строку с замаскированным номером"""
    if not any(char.isdigit() for char in number_type):
        return "Некорректный ввод данных"
    if "Счет" in number_type or "счет" in number_type:
        number_type_cleaned = number_type.replace("-", "").replace(" ", "")
        account_mask = "**" + number_type_cleaned[-4:]
        return f"Счет {account_mask}"
    number_type_cleaned = number_type.replace("-", "").replace(" ", "")

    def separate_card_number(number_type_input: str) -> str:
        match = re.search(r"(\D+)(\d+)", number_type_input)
        if match:
            card_type = match.group(1)
            card_number = match.group(2)
            return f"{card_type} {card_number}"
        else:
            return "Ошибка"

    rebuilded_number_type = separate_card_number(number_type_cleaned)
    splited_number_type = rebuilded_number_type.split()
    number_mask = (
        splited_number_type[1][0:4] + " " + splited_number_type[1][4:6] + "** ****" + " " + splited_number_type[1][-4:]
    )
    return f"{splited_number_type[0]} {number_mask}"


def get_date(date: str) -> str:
    """Функция принимает строку с датой и возвращает дату в другом формате"""
    if date == "" or "T" not in date:
        return "Некорректный ввод"
    return f"{date[8:10]}.{date[5:7]}.{date[0:4]}"
