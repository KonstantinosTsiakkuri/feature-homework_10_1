import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "index,mask",
    [
        (0, "**4305"),
        (1, "**4366"),
        (2, "**4377"),
        (3, "**4305"),
        (4, "Некорректный ввод"),
        (5, "Некорректный ввод"),
    ],
)
def test_get_mask_account(account_numbers, index, mask):
    """Тестирование функции get_mask_account"""
    account = account_numbers[index]
    assert get_mask_account(account) == mask


@pytest.mark.parametrize(
    "index,expected",
    [
        (0, "Некорректный ввод"),
        (1, "7365 41** **** 3587"),
        (2, "7365 41** **** 3587"),
        (3, "7365 41** **** 3587"),
        (4, "7365 41** **** 3587"),
        (5, "Некорректный ввод"),
    ],
)
def test_get_mask_card_number(card_numbers, index, expected):
    """Тестирование функции get_mask_card_number"""
    number = card_numbers[index]
    assert get_mask_card_number(number) == expected
