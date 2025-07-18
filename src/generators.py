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
    transactions_list: List[Dict[str, Any]] = []  # pragma: no cover
    processed_transactions = int(input("Количество транзакций для обработки"))  # pragma: no cover
    usd_transactions = filter_by_currency(transactions_list, "USD")  # pragma: no cover
    for _ in range(processed_transactions):  # pragma: no cover
        try:  # pragma: no cover
            print(next(usd_transactions))  # pragma: no cover
        except StopIteration:  # pragma: no cover
            print("Окончание обработки")  # pragma: no cover
            break  # pragma: no cover

    descriptions = transaction_descriptions(transactions_list)  # pragma: no cover
    processed_transactions_descriptions = int(input("Количество транзакций для обработки"))  # pragma: no cover
    for _ in range(processed_transactions_descriptions):  # pragma: no cover
        try:  # pragma: no cover
            print(next(descriptions))  # pragma: no cover
        except StopIteration:  # pragma: no cover
            print("Окончание обработки")  # pragma: no cover
            break  # pragma: no cover
