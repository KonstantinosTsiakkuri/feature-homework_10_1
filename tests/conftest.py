import pytest


@pytest.fixture
def account_numbers():
    """Фикстура, генерирующая входные данные для функции get_mask_account"""
    return [
        "73654108430135874305",
        "7365 4108 4301 3587 4366",
        "7365-4108-4301-3587-4377",
        "A-73654108430135874305-B",
        "736541084374305",
        "",
    ]


@pytest.fixture
def card_numbers():
    """Фикстура, генерирующая входные данные для функции get_mask_card_number"""
    return [
        "",
        "7365410843013587",
        "7365 4108 4301 3587",
        "7365-4108-4301-3587",
        "A-7365410843013587-B",
        "736541084374305",
    ]


@pytest.fixture
def number_type():
    """Фикстура, генерирующая входные данные для функции mask_account_card"""
    return ["Visa Platinum 7000 7922 8960 6361", "Maestro 7000-7922-8960-6361", "Счет 7000792289606361"]


@pytest.fixture
def dates():
    """Фикстура, генерирующая входные данные для функции get_date"""
    return ["2024-03-11T02:26:18.671407", "0001-01-01T00:00:00.000000", "2024-03-11", ""]


@pytest.fixture
def states():
    """Фикстура, генерирующая входные данные для функции filter_by_state"""
    return ["EXECUTED", "executed", "CANCELED", "", "ejdfejfijeifjie"]


@pytest.fixture
def transactions():
    """Фикстура, генерирующая входные данные для функции sort_by_date"""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def transactions_for_generators():
    """Фикстура, генерирующая входные данные для функций filter_by_currency и  transaction_descriptions"""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]
