from typing import cast

from src.CSV_reader import CSV_reader
from src.Excel_reader import excel_reader
from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date
from src.utils import function as read_json_transactions
from src.widget import get_date, mask_account_card

STATUSES = ("EXECUTED", "CANCELED", "PENDING")
DATA_READERS = {
    "1": ("JSON", read_json_transactions),
    "2": ("CSV", CSV_reader),
    "3": ("XLSX", excel_reader),
}


def get_amount_and_currency_code(transaction: dict) -> tuple[str, str]:
    """Возвращает сумму и код валюты транзакции независимо от формата источника (JSON/CSV/XLSX)"""
    operation_amount = transaction.get("operationAmount")
    if operation_amount:
        return str(operation_amount.get("amount", "")), operation_amount.get("currency", {}).get("code", "")
    return str(transaction.get("amount", "")), transaction.get("currency_code", "")


def format_transaction(transaction: dict) -> str:
    """Форматирует одну транзакцию для вывода в консоль"""
    date_line = f"{get_date(transaction.get('date', ''))} {transaction.get('description', '')}"
    accounts = [
        cast(str, mask_account_card(value))
        for value in (transaction.get("from"), transaction.get("to"))
        if isinstance(value, str) and value
    ]
    accounts_line = " -> ".join(accounts)
    amount, currency_code = get_amount_and_currency_code(transaction)
    currency_label = "руб." if currency_code == "RUB" else currency_code
    return f"{date_line}\n{accounts_line}\nСумма: {amount} {currency_label}"


def ask_yes_no(question: str) -> bool:
    """Запрашивает у пользователя ответ да/нет, повторяя вопрос при некорректном вводе"""
    while True:
        answer = input(question).strip().lower()
        if answer in ("да", "нет"):
            return answer == "да"
        print("Программа: Пожалуйста, введите 'Да' или 'Нет'")


def choose_data_source() -> list[dict]:
    """Приветствует пользователя, запрашивает источник данных и возвращает список транзакций"""
    print(
        "Программа: Привет! Добро пожаловать в программу работы\n"
        "с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )
    while True:
        choice = input().strip()
        if choice in DATA_READERS:
            label, reader = DATA_READERS[choice]
            print(f"Программа: Для обработки выбран {label}-файл.")
            return reader() or []
        print("Программа: Пункт меню недоступен, повторите ввод.")


def choose_status(transactions: list[dict]) -> list[dict]:
    """Запрашивает статус фильтрации, пока не будет введён один из допустимых, и возвращает отфильтрованный список"""
    while True:
        print(
            "Программа: Введите статус, по которому необходимо выполнить фильтрацию.\n"
            f"Доступные для фильтровки статусы: {', '.join(STATUSES)}"
        )
        status = input().strip()
        if status.upper() in STATUSES:
            print(f'Программа: Операции отфильтрованы по статусу "{status.upper()}"')
            filtered = filter_by_state(transactions, status)
            return filtered if isinstance(filtered, list) else []
        print(f'Программа: Статус операции "{status}" недоступен.')


def apply_sorting(transactions: list[dict]) -> list[dict]:
    """Уточняет у пользователя направление сортировки по дате и применяет её при необходимости"""
    if not ask_yes_no("Программа: Отсортировать операции по дате? Да/Нет\n"):
        return transactions
    while True:
        direction = input("Программа: Отсортировать по возрастанию или по убыванию?\n").strip().lower()
        if direction in ("по возрастанию", "по убыванию"):
            return sort_by_date(transactions, reverse=(direction == "по убыванию"))
        print("Программа: Пожалуйста, введите 'по возрастанию' или 'по убыванию'")


def apply_currency_filter(transactions: list[dict]) -> list[dict]:
    """Уточняет у пользователя, оставлять ли только рублёвые транзакции, и применяет фильтр"""
    if not ask_yes_no("Программа: Выводить только рублевые транзакции? Да/Нет\n"):
        return transactions
    return [t for t in transactions if get_amount_and_currency_code(t)[1] == "RUB"]


def apply_description_filter(transactions: list[dict]) -> list[dict]:
    """Уточняет у пользователя слово для поиска в описании и применяет фильтр"""
    if not ask_yes_no("Программа: Отфильтровать список транзакций по определенному слову\nв описании? Да/Нет\n"):
        return transactions
    word = input("Программа: Введите слово для поиска в описании\n")
    return process_bank_search(transactions, word)


def print_category_counts(transactions: list[dict]) -> None:
    """Уточняет у пользователя список категорий и выводит подсчёт операций по ним"""
    if not ask_yes_no("Программа: Вывести подсчет количества операций по категориям? Да/Нет\n"):
        return
    categories_input = input("Программа: Введите категории через запятую\n")
    categories = [category.strip() for category in categories_input.split(",") if category.strip()]
    counts = process_bank_operations(transactions, categories)
    print("Программа: Подсчет операций по категориям:")
    for category, count in counts.items():
        print(f"{category}: {count}")


def print_transactions(transactions: list[dict]) -> None:
    """Выводит итоговый список транзакций либо сообщение о пустой выборке"""
    print("Программа: Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши\nусловия фильтрации")
        return
    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for transaction in transactions:
        print(format_transaction(transaction))
        print()


def main() -> None:
    """Основная функция, связывающая функциональность проекта работы с банковскими транзакциями"""
    transactions = choose_data_source()
    transactions = choose_status(transactions)
    transactions = apply_sorting(transactions)
    transactions = apply_currency_filter(transactions)
    transactions = apply_description_filter(transactions)
    print_category_counts(transactions)
    print_transactions(transactions)


if __name__ == "__main__":  # pragma: no cover
    main()
