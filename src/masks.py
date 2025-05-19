def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    cleaned_number = card_number.replace("A-", "").replace("-B", "").replace(" ", "").replace("-", "")
    card_number_mask = cleaned_number[0:4] + " " + cleaned_number[4:6] + "** **** " + cleaned_number[-4:]
    if card_number == "" or len(cleaned_number) != 16:
        return "Некорректный ввод"
    return card_number_mask


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    cleaned_number = account_number.replace("A-", "").replace("-B", "")
    account_mask = "**" + cleaned_number[-4:]
    if account_number == "" or len(cleaned_number) < 16:
        return "Некорректный ввод"
    return account_mask
