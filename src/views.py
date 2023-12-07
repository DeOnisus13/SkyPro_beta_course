import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from config import JSON_OUT_PATH, USER_SETTINGS_PATH, XLS_FILE_PATH


def get_hello_to_time():
    current_date_time = datetime.now()
    if 0 <= current_date_time.hour < 6:
        return "Доброй ночи"
    elif 6 <= current_date_time.hour < 12:
        return "Доброе утро"
    elif 12 <= current_date_time.hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def read_xls_file(file_path):
    # Исходный файл
    df_raw = pd.read_excel(file_path)
    # Фильтрует исходный файл по статусу операции
    df_ok = df_raw[df_raw["Статус"] == "OK"]
    # Преобразуем дату в столбце в объект DateTime
    df_ok.loc[:, "Дата операции"] = pd.to_datetime(df_ok["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    return df_ok


def get_card_info(file_path, end_date=None, start_date=None):
    # Из функции получаем обработанный файл
    df_ok = read_xls_file(file_path)
    # Фильтруем по не пустому номеру карты
    df_ok_not_null = df_ok[df_ok[["Номер карты"]].notnull().all(1)]

    # Фильтр DataFrame по дате
    filtered_data = df_ok_not_null[
        (df_ok_not_null["Дата операции"] >= start_date) & (df_ok_not_null["Дата операции"] <= end_date)
    ]

    # Делаем из DataFrame список словарей
    df_dict = filtered_data.to_dict("records")
    # Получаем список номеров карт
    df_card_numbers = [df_dict[i]["Номер карты"] for i in range(len(df_dict))]
    list_of_cards = list(set(df_card_numbers))

    total_summ_for_card = []
    cashback_for_card = []

    # Проходим циклом по списку карт в списке словарей и вычисляем общую сумму и кэшбэк по каждой из карт
    for card in list_of_cards:
        summ = 0
        cashback = 0
        for record in df_dict:
            if record["Номер карты"] == card and record["Сумма платежа"] < 0:
                summ += abs(record["Сумма платежа"])
                if not record["Кэшбэк"].is_integer():
                    cashback += abs(record["Сумма платежа"]) / 100
                else:
                    cashback += record["Кэшбэк"]
        total_summ_for_card.append(round(summ, 2))
        cashback_for_card.append(round(cashback, 2))

    result_list_of_cards = []

    # В цикле составляем список словарей с результатами по каждой из карт
    for card in range(len(list_of_cards)):
        result_dict_for_card = {
            "last_digits": list_of_cards[card],
            "total_spent": total_summ_for_card[card],
            "cashback": cashback_for_card[card],
        }
        result_list_of_cards.append(result_dict_for_card)
    return result_list_of_cards


def get_top_5_largest_payments(file_path, end_date=None, start_date=None):
    df = read_xls_file(file_path)
    # Фильтр DataFrame по дате
    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    # Перевод DataFrame в список словарей
    df_dicts = filtered_df.to_dict("records")
    # Приведение объекта DateTime к строке
    for record in df_dicts:
        record["Дата операции"] = datetime.strftime(record["Дата операции"], "%d.%m.%Y %H:%M:%S")
    # Сортировка списка словарей по убыванию
    sorted_df_dicts = sorted(df_dicts, key=lambda i: abs(i["Сумма платежа"]), reverse=True)

    result_top_5_payments = []
    # Получение 5 транзакций и запись словаря в итоговый список
    if len(sorted_df_dicts) >= 5:
        for x in range(5):
            dict_for_payment = {
                "date": sorted_df_dicts[x]["Дата операции"],
                "amount": sorted_df_dicts[x]["Сумма платежа"],
                "category": sorted_df_dicts[x]["Категория"],
                "description": sorted_df_dicts[x]["Описание"],
            }
            result_top_5_payments.append(dict_for_payment)
    else:
        for x in range(len(sorted_df_dicts)):
            dict_for_payment = {
                "date": sorted_df_dicts[x]["Дата операции"],
                "amount": sorted_df_dicts[x]["Сумма платежа"],
                "category": sorted_df_dicts[x]["Категория"],
                "description": sorted_df_dicts[x]["Описание"],
            }
            result_top_5_payments.append(dict_for_payment)
    return result_top_5_payments


def get_currency_rate(currencies):
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        currency_data = response.json()
        result_currency_list = []

        for currency in currencies:
            if currency in currency_data["Valute"]:
                currency_rate = {
                    "currency": currency,
                    "rate": currency_data["Valute"][currency]["Value"],
                }
                result_currency_list.append(currency_rate)
        return result_currency_list

    except Exception as error:
        print(f"Возникла ошибка {type(error).__name__}")


def get_stock_price(stocks):
    try:
        load_dotenv()
        api_key = os.getenv("API_KEY")
        stocks_list = []
        for stock in stocks:
            url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={api_key}"
            response = requests.get(url)
            response_json = response.json()
            stocks_dict = {"stock": stock, "price": response_json["c"]}
            stocks_list.append(stocks_dict)
        return stocks_list

    except Exception as error:
        print(f"Возникла ошибка {type(error).__name__}")


def generate_main_view_json(input_date=None, date_first=None):
    if not date_first:
        date_first = input_date[0:8] + "01 00:00:00"
    start = datetime.strptime(date_first, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")

    with open(USER_SETTINGS_PATH, "r", encoding="utf-8") as file:
        user_settings = json.load(file)

    user_currencies = user_settings.get("user_currencies", [])
    user_stocks = user_settings.get("user_stocks", [])

    report = {
        "greeting": get_hello_to_time(),
        "cards": get_card_info(XLS_FILE_PATH, end, start),
        "top_transactions": get_top_5_largest_payments(XLS_FILE_PATH, end, start),
        "currency_rates": get_currency_rate(user_currencies),
        "stock_prices": get_stock_price(user_stocks),
    }

    with open(JSON_OUT_PATH, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    generate_main_view_json("2020-03-14 16:00:00")
