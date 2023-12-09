from datetime import datetime

import pandas as pd

from config import XLS_FILE_PATH


def investment_bank(transactions, year_month, limit):
    date = datetime.strptime(year_month, "%Y-%m")

    for transaction in transactions:
        transaction["Дата операции"] = datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")

    investments = []
    for xx in transactions:
        if xx["Дата операции"].year == date.year and xx["Дата операции"].month == date.month:
            investments.append(xx)

    result_investment = list(
        map(
            lambda price: ((price["Сумма платежа"] // limit) * limit) + limit - price["Сумма платежа"],
            investments,
        )
    )

    return sum(result_investment)


if __name__ == "__main__":
    df_raw = pd.read_excel(XLS_FILE_PATH)
    df_ok = df_raw[df_raw["Статус"] == "OK"]
    df_ok_not_null = df_ok[df_ok[["Номер карты"]].notnull().all(1)]
    ddf = df_ok_not_null[df_ok_not_null["Сумма платежа"] < 0]
    df_dict1 = ddf.to_dict("records")
    print(investment_bank(df_dict1, "2020-10", 50))
