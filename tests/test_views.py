from datetime import datetime

from src.views import get_hello_to_time


def test_get_hello_to_time():
    assert get_hello_to_time() in ["Добрый день", "Доброе утро", "Добрый вечер", "Доброй ночи"]
    