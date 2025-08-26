import os
from unittest.mock import mock_open, patch

from src.utils import function


@patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
@patch("json.load", return_value=[{"id": 1, "amount": 100}])
def test_function(mock_json_load, mock_open):
    """Тестовая функция к функции function"""
    result = function()
    assert result == [{"id": 1, "amount": 100}], "Функция должна возвращать список со словарем"
    mock_open.assert_called_once_with(os.getenv("PATH_TO_JSON"), encoding="utf-8")
    mock_json_load.assert_called_once()
