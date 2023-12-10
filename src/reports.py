import datetime
from functools import wraps
from pathlib import Path
from typing import Any

import pandas as pd


def report_to_file(func: Any) -> Any:
    """
    Декоратор без параметра, который записывает результат функции в excel файл по указанному пути с указанным именем.
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)

        saving_place = Path(Path(__file__).parent.parent.joinpath("data", f"{func.__name__}_report.xlsx"))

        result.to_excel(saving_place, index=False)

        return result

    return wrapper


@report_to_file
def category_filter(transactions: pd.DataFrame, category: str, date: str = "") -> pd.DataFrame:
    """
    Функция фильтрующая транзакции по указанной категории за определенный временной период.
    На вход поступает DataFrame с данными о транзакциях,
        Категория транзакций, которую нужно отфильтровать и
        Дата в формате "YYYY-MM-DD HH:MM:SS" для определения временного интервала.
    Выход функции - DataFrame с отфильтрованными транзакциями.
    """
    if date == "":
        date_obj = datetime.datetime.now()
    else:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    start_date = (date_obj - datetime.timedelta(days=90)).strftime("%Y.%m.%d")
    end_date = date_obj.strftime("%Y.%m.%d")

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    df_by_category = transactions.loc[
        (transactions["Статус"] == "OK")
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= end_date)
        & (transactions["Категория"] == category)
    ]

    return df_by_category
