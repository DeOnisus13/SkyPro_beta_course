import datetime
from functools import wraps
from pathlib import Path

import pandas as pd

from config import XLS_FILE_PATH


def report_to_file(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        saving_place = Path(
                    Path(__file__).parent.parent.joinpath("data", f"{func.__name__}_report.xlsx")
                )

        result.to_excel(saving_place, index=False)

        return result

    return wrapper


@report_to_file
def category_filter(transactions: pd.DataFrame, category: str, date: str = "") -> pd.DataFrame:
    """
    Функция фильтрующая транзакции по указанной категории за определенный временной период.
    :param transactions: DataFrame с данными о транзакциях.
    :param category: Категория транзакций, которую нужно отфильтровать.
    :param date: Дата в формате "YYYY-MM-DD HH:MM:SS" для определения временного интервала.
    :return: DataFrame с отфильтрованными транзакциями.
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


if __name__ == '__main__':
    df = pd.read_excel(XLS_FILE_PATH)
    category_filter(df, "Супермаркеты", "2020-05-06 14:00:00")
