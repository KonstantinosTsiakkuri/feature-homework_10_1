import pytest

from src.processing import filter_by_state, process_bank_operations, process_bank_search, sort_by_date

dict_list = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


@pytest.mark.parametrize(
    "index, expected",
    [
        (
            0,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            1,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            2,
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        (3, "Некорректный статус"),
        (4, "Некорректный статус"),
    ],
)
def test_filter_by_state(states, index, expected):
    """Тестирование функции filter_by_state"""
    state = states[index]
    assert filter_by_state(dict_list, state) == expected


@pytest.mark.parametrize(
    "reverse,expected",
    [
        (
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
    ],
)
def test_sort_by_date(transactions, reverse, expected):
    assert sort_by_date(transactions, reverse=reverse) == expected


@pytest.mark.parametrize(
    "search, expected_ids",
    [
        ("Перевод", [939719570, 142264268, 873106923, 895315941, 594226727]),
        ("перевод", [939719570, 142264268, 873106923, 895315941, 594226727]),
        ("карту", [895315941]),
        ("не существует", []),
    ],
)
def test_process_bank_search(transactions_for_generators: list[dict], search: str, expected_ids: list[int]) -> None:
    """Тестирование функции process_bank_search"""
    result = process_bank_search(transactions_for_generators, search)
    assert [transaction["id"] for transaction in result] == expected_ids


def test_process_bank_operations(transactions_for_generators: list[dict]) -> None:
    """Тестирование функции process_bank_operations"""
    categories = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Открытие вклада",
    ]
    expected = {
        "Перевод организации": 2,
        "Перевод со счета на счет": 2,
        "Перевод с карты на карту": 1,
        "Открытие вклада": 0,
    }
    assert process_bank_operations(transactions_for_generators, categories) == expected
