from src.services import investment_bank


def test_investment_bank_calculation():
    transactions = [
        {"Дата операции": "01.01.2022 12:00:00", "Сумма платежа": 198},
        {"Дата операции": "15.01.2022 14:30:00", "Сумма платежа": 299},
        {"Дата операции": "25.01.2022 08:45:00", "Сумма платежа": 1015}
    ]
    year_month = "2022-01"
    limit = 10
    assert investment_bank(transactions, year_month, limit) == 8


def test_investment_bank_empty_transactions():
    transactions = []
    year_month = "2022-01"
    limit = 500
    assert investment_bank(transactions, year_month, limit) == 0


def test_investment_bank_no_matching_transactions():
    transactions = [
        {"Дата операции": "01.02.2022 12:00:00", "Сумма платежа": 100},
        {"Дата операции": "15.03.2022 14:30:00", "Сумма платежа": 200}
    ]
    year_month = "2022-01"
    limit = 500
    assert investment_bank(transactions, year_month, limit) == 0
