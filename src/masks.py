def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    card_number_mask = "" + card_number[0:4] + " " + card_number[5:7] + "** **** " + card_number[12:]
    return card_number_mask


card_number = input()
print(get_mask_card_number(card_number))


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    account_mask = "**" + account_number[-4:]
    return account_mask


account_number = input()
print(get_mask_account(account_number))
