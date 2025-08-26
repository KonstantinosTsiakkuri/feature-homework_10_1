import json
from unittest.mock import patch

import pandas as pd

from src.Excel_reader import excel_reader


@patch("pandas.read_excel")
def test_excel_reader(mock_read_excel):
    mock_data = pd.DataFrame({"id": [1, 2], "amount": [100, 200]})
    mock_read_excel.return_value = mock_data
    expected_result = json.dumps(mock_data.to_dict(orient="records"), ensure_ascii=False, indent=4)
    result = excel_reader("dummy_path")
    assert result == expected_result
    mock_read_excel.assert_called_once_with("dummy_path")
