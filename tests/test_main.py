import pytest

import main

SAMPLE_TRANSACTIONS = [
    {
        "id": 1,
        "state": "EXECUTED",
        "date": "2019-12-08T10:00:00.000000",
        "operationAmount": {"amount": "40542", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Открытие вклада",
        "from": "Счет 89876543214321",
    },
    {
        "id": 2,
        "state": "EXECUTED",
        "date": "2019-11-12T10:00:00.000000",
        "operationAmount": {"amount": "130", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "MasterCard 7771271111113727",
        "to": "Visa Platinum 1293381111119203",
    },
    {
        "id": 3,
        "state": "CANCELED",
        "date": "2018-07-18T10:00:00.000000",
        "operationAmount": {"amount": "8390", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 7492651111117202",
    },
]

FLAT_TRANSACTION = {
    "id": 4,
    "state": "EXECUTED",
    "date": "2018-06-03T10:00:00.000000",
    "amount": "8200",
    "currency_code": "EUR",
    "description": "Перевод со счета на счет",
    "from": "Счет 12345678902935",
    "to": "Счет 89876543214321",
}


def test_get_amount_and_currency_code_nested() -> None:
    """Проверяем извлечение суммы и валюты для вложенного (JSON) формата"""
    assert main.get_amount_and_currency_code(SAMPLE_TRANSACTIONS[0]) == ("40542", "RUB")


def test_get_amount_and_currency_code_flat() -> None:
    """Проверяем извлечение суммы и валюты для плоского (CSV/XLSX) формата"""
    assert main.get_amount_and_currency_code(FLAT_TRANSACTION) == ("8200", "EUR")


def test_format_transaction_single_account() -> None:
    """Проверяем форматирование транзакции с одним счетом и рублёвой суммой"""
    result = main.format_transaction(SAMPLE_TRANSACTIONS[0])
    assert result == "08.12.2019 Открытие вклада\nСчет **4321\nСумма: 40542 руб."


def test_format_transaction_ignores_missing_account_as_nan() -> None:
    """Проверяем, что NaN (пропуск ячейки в XLSX) в поле from/to не приводит к падению"""
    transaction: dict = {
        "id": 5,
        "date": "2019-12-08T10:00:00.000000",
        "amount": "100",
        "currency_code": "RUB",
        "description": "Тест",
        "from": float("nan"),
        "to": "Счет 89876543214321",
    }
    result = main.format_transaction(transaction)
    assert result == "08.12.2019 Тест\nСчет **4321\nСумма: 100 руб."


def test_format_transaction_two_accounts() -> None:
    """Проверяем форматирование транзакции с переводом между двумя счетами"""
    result = main.format_transaction(SAMPLE_TRANSACTIONS[1])
    assert "MasterCard 7771 27** **** 3727 -> VisaPlatinum 1293 38** **** 9203" in result
    assert "Сумма: 130 USD" in result


def test_choose_data_source_invalid_then_valid(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """Проверяем повторный запрос при некорректном пункте меню источника данных"""
    monkeypatch.setitem(main.DATA_READERS, "1", ("JSON", lambda: SAMPLE_TRANSACTIONS))
    inputs = iter(["9", "1"])
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))
    result = main.choose_data_source()
    assert result == SAMPLE_TRANSACTIONS
    assert "Пункт меню недоступен" in capsys.readouterr().out


def test_choose_status_invalid_then_valid(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяем повторный запрос статуса без падения программы при неверном значении"""
    inputs = iter(["test", "executed"])
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))
    result = main.choose_status(SAMPLE_TRANSACTIONS)
    assert [t["id"] for t in result] == [1, 2]
    assert 'Статус операции "test" недоступен' in capsys.readouterr().out


def test_apply_sorting_ascending(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяем сортировку по возрастанию даты при подтверждении пользователем"""
    inputs = iter(["да", "по возрастанию"])
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))
    result = main.apply_sorting(SAMPLE_TRANSACTIONS)
    assert [t["id"] for t in result] == [3, 2, 1]


def test_apply_sorting_declined(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяем, что список не меняется при отказе от сортировки"""
    monkeypatch.setattr("builtins.input", lambda *a: "нет")
    result = main.apply_sorting(SAMPLE_TRANSACTIONS)
    assert result == SAMPLE_TRANSACTIONS


def test_apply_currency_filter_only_rub(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяем фильтрацию только рублёвых транзакций"""
    monkeypatch.setattr("builtins.input", lambda *a: "да")
    result = main.apply_currency_filter(SAMPLE_TRANSACTIONS)
    assert [t["id"] for t in result] == [1, 3]


def test_apply_description_filter(monkeypatch: pytest.MonkeyPatch) -> None:
    """Проверяем фильтрацию транзакций по слову в описании"""
    inputs = iter(["да", "вклад"])
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))
    result = main.apply_description_filter(SAMPLE_TRANSACTIONS)
    assert [t["id"] for t in result] == [1]


def test_print_category_counts(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """Проверяем вывод подсчёта операций по категориям"""
    inputs = iter(["да", "Открытие вклада, Перевод организации"])
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))
    main.print_category_counts(SAMPLE_TRANSACTIONS)
    output = capsys.readouterr().out
    assert "Открытие вклада: 1" in output
    assert "Перевод организации: 1" in output


def test_print_transactions_empty(capsys: pytest.CaptureFixture) -> None:
    """Проверяем сообщение при пустой выборке транзакций"""
    main.print_transactions([])
    output = capsys.readouterr().out
    assert "Не найдено ни одной транзакции" in output


def test_print_transactions_non_empty(capsys: pytest.CaptureFixture) -> None:
    """Проверяем вывод количества и содержимого транзакций непустой выборки"""
    main.print_transactions(SAMPLE_TRANSACTIONS[:1])
    output = capsys.readouterr().out
    assert "Всего банковских операций в выборке: 1" in output
    assert "Открытие вклада" in output


def test_main_full_flow(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """Интеграционный тест полного сценария main() от выбора источника до вывода списка"""
    monkeypatch.setitem(main.DATA_READERS, "1", ("JSON", lambda: SAMPLE_TRANSACTIONS))
    inputs = iter(
        [
            "1",
            "EXECUTED",
            "да",
            "по возрастанию",
            "нет",
            "да",
            "вклад",
            "нет",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))
    main.main()
    output = capsys.readouterr().out
    assert "Открытие вклада" in output
    assert "Всего банковских операций в выборке: 1" in output


def test_main_empty_result(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """Интеграционный тест сценария, когда итоговая выборка оказывается пустой"""
    monkeypatch.setitem(main.DATA_READERS, "1", ("JSON", lambda: SAMPLE_TRANSACTIONS))
    inputs = iter(
        [
            "1",
            "EXECUTED",
            "нет",
            "нет",
            "да",
            "несуществующее слово",
            "нет",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda *a: next(inputs))
    main.main()
    output = capsys.readouterr().out
    assert "Не найдено ни одной транзакции" in output
