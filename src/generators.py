from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """Функция поочередно возвращает транзакции с заданной валютой"""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Функция поочередно возвращает описание транзакций"""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(first_number: int, second_number: int) -> Generator[str, None, None]:
    """Функция, генерирующая номера карт в заданном диапазоне"""
    for number in range(first_number, second_number + 1):
        card_number = str(number).zfill(16)
        formatted_card_number = f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
        yield formatted_card_number


if __name__ == "__main__":
    transactions_list: List[Dict[str, Any]] = []  # Здесь должны быть твои данные транзакций
    processed_transactions = int(input("Количество транзакций для обработки"))
    usd_transactions = filter_by_currency(transactions_list, "USD")
    for _ in range(processed_transactions):
        try:
            print(next(usd_transactions))
        except StopIteration:
            print("Окончание обработки")
            break

    descriptions = transaction_descriptions(transactions_list)
    processed_transactions_descriptions = int(input("Количество транзакций для обработки"))
    for _ in range(processed_transactions_descriptions):
        try:
            print(next(descriptions))
        except StopIteration:
            print("Окончание обработки")
            break
