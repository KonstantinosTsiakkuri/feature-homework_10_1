import pytest

from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.widget import get_date, mask_account_card


# Тестирование функции get_mask_account
@pytest.mark.parametrize(
    "account,mask",
    [
        ("73654108430135874305", "**4305"),
        ("7365 4108 4301 3587 4366", "**4366"),
        ("7365-4108-4301-3587-4377", "**4377"),
        ("A-73654108430135874305-B", "**4305"),
        ("736541084374305", "Некорректный ввод"),
        ("", "Некорректный ввод"),
    ],
)
def test_get_mask_account(account, mask):
    assert get_mask_account(account) == mask


# Тестирование функции get_mask_card_number
@pytest.mark.parametrize(
    "number,expected",
    [
        ("", "Некорректный ввод"),
        ("7365410843013587", "7365 41** **** 3587"),
        ("7365 4108 4301 3587", "7365 41** **** 3587"),
        ("7365-4108-4301-3587", "7365 41** **** 3587"),
        ("A-7365410843013587-B", "7365 41** **** 3587"),
        ("736541084374305", "Некорректный ввод"),
    ],
)
def test_get_mask_card_number(number, expected):
    assert get_mask_card_number(number) == expected


# !!!!!!!Тестирование функции mask_account_card
@pytest.mark.parametrize(
    "number_type,expected",
    [
        ("Visa Platinum 7000 7922 8960 6361", "VisaPlatinum 7000 79** **** 6361"),
        ("Maestro 7000-7922-8960-6361", "Maestro 7000 79** **** 6361"),
        ("Счет 7000792289606361", "Счет **6361"),
    ],
)
def test_mask_account_card(number_type, expected):
    assert mask_account_card(number_type) == expected


# Тестирование функции get_date
@pytest.mark.parametrize(
    "date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("0001-01-01T00:00:00.000000", "01.01.0001"),
        ("2024-03-11", "Некорректный ввод"),
        ("", "Некорректный ввод"),
    ],
)
def test_get_date(date, expected):
    assert get_date(date) == expected


#  Тестирование функции filter_by_state
dict_list = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


@pytest.mark.parametrize(
    "state, expected",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "executed",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        ("", "Некорректный статус"),
        ("ejdfejfijeifjie", "Некорректный статус"),
    ],
)
def test_filter_by_state(state, expected):
    assert filter_by_state(dict_list, state) == expected


# Тестирование функции sort_by_date
dict_list = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


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
def test_sort_by_date(reverse, expected):
    assert sort_by_date(dict_list, reverse=reverse) == expected
