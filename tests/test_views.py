from datetime import datetime

import pytest
import requests
from src.views import get_hello_to_time, get_currency_rate


def test_get_hello_to_time():
    if get_hello_to_time() == 4:
        assert get_hello_to_time() == "Доброй ночи"
    elif get_hello_to_time() == 8:
        assert get_hello_to_time() == "Доброе утро"
    elif get_hello_to_time() == 14:
        assert get_hello_to_time() == "Добрый день"
    elif get_hello_to_time() == 20:
        assert get_hello_to_time() == "Добрый вечер"


def test_get_currency_rate_valid_input():
    currencies = ["USD", "EUR"]
    response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    currency_data = response.json()
    expected_result = [
        {"currency": "USD", "rate": currency_data["Valute"]["USD"]["Value"]},
        {"currency": "EUR", "rate": currency_data["Valute"]["EUR"]["Value"]}
    ]
    assert get_currency_rate(currencies) == expected_result


def test_get_currency_rate_empty_input():
    currencies = []
    expected_result = []
    assert get_currency_rate(currencies) == expected_result
