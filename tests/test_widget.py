import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "index,expected",
    [
        (0, "VisaPlatinum 7000 79** **** 6361"),
        (1, "Maestro 7000 79** **** 6361"),
        (2, "Счет **6361"),
    ],
)
def test_mask_account_card(number_type, index, expected):
    """Тестирование функции mask_account_card"""
    number = number_type[index]
    assert mask_account_card(number) == expected


@pytest.mark.parametrize(
    "index, expected",
    [
        (0, "11.03.2024"),
        (1, "01.01.0001"),
        (2, "Некорректный ввод"),
        (3, "Некорректный ввод"),
    ],
)
def test_get_date(dates, index, expected):
    """Тестирование функции get_date"""
    date = dates[index]
    assert get_date(date) == expected
