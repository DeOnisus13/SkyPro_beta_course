from datetime import datetime
from typing import Any


def investment_bank(transactions: list[dict], year_month: str, limit: int) -> Any:
    """
    Функция "Инвестиционная копилка" для вычисления суммы, которую можно получить от округления платежей до заданного
    порога.
    На вход подаются список словарей, дата в формате год-месяц и число, до которого нужно округлить платеж.
    Выход - сумма, которую можно было отложить в инвестиции.
    """
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
