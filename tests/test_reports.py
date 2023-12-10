from config import XLS_FILE_PATH
from src.reports import category_filter
from src.views import read_xls_file


def test_filter_transactions() -> None:
    assert category_filter(read_xls_file(XLS_FILE_PATH), "Детские товары", "2021-10-15 16:00:00").shape == (
        4,
        15,
    )
    assert category_filter(read_xls_file(XLS_FILE_PATH), "Детские товары").shape == (0, 15)
