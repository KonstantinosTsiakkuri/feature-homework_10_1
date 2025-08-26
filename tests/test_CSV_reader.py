from unittest.mock import mock_open, patch

from src.CSV_reader import CSV_reader, CSV_to_json


@patch("builtins.open", new_callable=mock_open, read_data="id;amount\n1;100\n2;200\n")
def test_csv_reader(mock_file):
    """Тестирование функции, считывающей данные из CSV-файла"""
    expected_result = [{"id": "1", "amount": "100"}, {"id": "2", "amount": "200"}]
    result = CSV_reader("dummy_path")
    assert result == expected_result
    mock_file.assert_any_call("dummy_path", encoding="utf-8")


@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
def test_json_write(mock_json_dump, mock_file):
    """Тестирование функции, записывающей данные из CSV в json формат"""
    transactions = [{"id": "1", "amount": "100"}, {"id": "2", "amount": "200"}]
    CSV_to_json(transactions, "dummy_path.json")
    mock_file.assert_called_once_with("dummy_path.json", "w", encoding="utf-8")
    mock_json_dump.assert_called_once_with(transactions, mock_file(), ensure_ascii=False, indent=4)
