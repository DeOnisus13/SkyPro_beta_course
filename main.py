import pandas as pd

from config import XLS_FILE_PATH
from src.reports import category_filter
from src.services import investment_bank
from src.views import generate_main_view_json


def main():
    """
    Главная функция для объединения вызова всех функций
    """
    # Вызов функции генерации json файла для главной страницы
    generate_main_view_json("2020-03-14 16:00:00")

    # Вызов функции для сервисов
    df_raw = pd.read_excel(XLS_FILE_PATH)
    df_ok = df_raw[df_raw["Статус"] == "OK"]
    df_ok_not_null = df_ok[df_ok[["Номер карты"]].notnull().all(1)]
    df_sub_zero = df_ok_not_null[df_ok_not_null["Сумма платежа"] < 0]
    df_dict1 = df_sub_zero.to_dict("records")
    print(investment_bank(df_dict1, "2020-10", 50))

    # Вызов функции для отчетов
    df = pd.read_excel(XLS_FILE_PATH)
    category_filter(df, "Супермаркеты", "2020-05-15 00:00:00")


if __name__ == '__main__':
    main()
