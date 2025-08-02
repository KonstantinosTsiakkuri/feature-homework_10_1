import logging


def log(filename=None):
    """Декоратор для логирования вызовов функций."""

    def my_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)  # Вызываем функцию только один раз!
                message = f"{func.__name__} is ok, result is {result}"
                if filename:
                    logging.basicConfig(
                        filename=filename,
                        level=logging.DEBUG,
                        filemode="w",
                        format="%(asctime)s %(levelname)s %(funcName)s %(message)s",
                    )
                    logging.info(message)
                else:
                    print(message)
                return result
            except Exception as e:
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs {args}, {kwargs}"
                if filename:
                    logging.error(error_message)
                else:
                    print(error_message)
                raise  # Пробрасываем оригинальное исключение без изменений

        return wrapper

    return my_decorator
