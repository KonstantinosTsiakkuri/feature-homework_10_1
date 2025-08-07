from unittest.mock import mock_open, patch

from src.external_api import transaction_function


def test_transaction_function():
    """ Тестовая функция к функции transaction_function """
    with patch(
        "builtins.open", mock_open(read_data='[{"operationAmount": {"amount": "100", "currency": {"name": "USD"}}}]')
    ):
        with patch(
            "json.load", return_value=[{"operationAmount": {"amount": "100", "currency": {"name": "USD"}}}]
        ) as mock_json_load:

            with patch("requests.get") as mock_get:
                mock_get.return_value.status_code = 200
                mock_get.return_value.json.return_value = {"result": 7500}

                results = list(transaction_function())

                assert results == ["7500 руб"], "Функция должна возвращать список с конвертированной суммой"
                mock_get.assert_called_once()
                mock_json_load.assert_called_once()
