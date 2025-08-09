import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(
    "C:\\Users\\olasp\\Desktop\\python projects\\widget_project_2\\logs\\masks.log", mode="w", encoding="utf-8"
)
logger.addHandler(file_handler)
file_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)


logger.info("Начало работы модуля")


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""
    logger.info("Обработка комера карты")
    cleaned_number = card_number.replace("A-", "").replace("-B", "").replace(" ", "").replace("-", "")
    card_number_mask = cleaned_number[0:4] + " " + cleaned_number[4:6] + "** **** " + cleaned_number[-4:]
    if card_number == "" or len(cleaned_number) != 16:
        logger.info("Проверка номера карты на корректность ввода")
        return "Некорректный ввод"
    return card_number_mask


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску."""
    logger.info("Обработка номера счета")
    cleaned_number = account_number.replace("A-", "").replace("-B", "")
    account_mask = "**" + cleaned_number[-4:]
    if account_number == "" or len(cleaned_number) < 16:
        logger.info("Проверка корректности номера счета")
        return "Некорректный ввод"
    return account_mask
