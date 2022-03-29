from src.main import getAllTransactions
from src.initial_filters import over_minimum_quantity
from src.has_income import complete_date_list
from src.second_stage import filter_high_income_words, filter_medium_income_words

def main_santander(json_data):

    initial_transaction_list = getAllTransactions(json_data)
    list_after_minimum = over_minimum_quantity(initial_transaction_list, json_data['parametros']['monto_minimo_tranzado'])

    HI_INCOME, HI_VALIDITY = high_income_analysis(get_transactions_by_month(list_after_minimum), json_data['parametros']['high_income_words'], json_data['parametros']['ventana_high_income'])
    MI_INCOME, MI_VALIDITY = medium_income_analysis(get_transactions_by_month(list_after_minimum), json_data['parametros']['medium_income_words'], json_data['parametros']['ventana_medium_income'])

    result = {
        'high_income_analysis_income' : HI_INCOME,
        'high_income_analysis_client_status' : HI_VALIDITY,
        'medium_income_analysis_income' : MI_INCOME,
        'medium_income_analysis_client_status' : MI_VALIDITY
    }

    json_data['income']['income_test_data'] = result
    return json_data

def high_income_analysis(transactions_by_month_data, high_income_word_list, considered_window):

    transactions_by_month = transactions_by_month_data[0]

    if len(transactions_by_month) <= considered_window:
        return 0, False #0 income, cliente no califica (False status)

    dateList = transactions_by_month_data[1][-considered_window:]

    transactions_by_month_2 = transactions_by_month.copy()

    for date in transactions_by_month_2.keys():
        if date not in dateList:
            del transactions_by_month[date]

    input = []
    for transaction_list in transactions_by_month.values():
        input+=transaction_list

    left_out, HI_TRANSACTIONS = filter_high_income_words(input, high_income_word_list)

    avg_by_month = dict()

    for date in dateList:
        for transaction in HI_TRANSACTIONS:
            if int("".join(transaction["date"].split("-")[:2])) == date:
                try:
                    avg_by_month[date].append(transaction)
                except:
                    avg_by_month[date] = [transaction]

    avg_by_month_2 = avg_by_month.copy()

    for k in avg_by_month_2.keys():
        avg_by_month[k] = sum(avg_by_month_2[k])

    monthly_average = sum([x for x in avg_by_month.values()]) / considered_window

    valid_income_months_counter = 0
    plus_30 = monthly_average * 1.3
    minus_30 = monthly_average * 0.7

    for k in avg_by_month.keys():
        if minus_30 <= avg_by_month[k] < plus_30:
            valid_income_months_counter += 1
        else:
            avg_by_month[k] = 0

    if valid_income_months_counter == 3:
        return round(monthly_average), True
    elif valid_income_months_counter == 2:
        return round((sum(avg_by_month.values()) / 2) * 0.8), True
    else:
        return 0, False

def medium_income_analysis(transactions_by_month_data, medium_income_word_list, considered_window = 6):

    transactions_by_month = transactions_by_month_data[0]

    if len(transactions_by_month) <= considered_window:
        return 0, False  # 0 income, cliente no califica (False status)

    dateList = transactions_by_month_data[1][-considered_window:]

    transactions_by_month_2 = transactions_by_month.copy()

    for date in transactions_by_month_2.keys():
        if date not in dateList:
            del transactions_by_month[date]

    input = []
    for transaction_list in transactions_by_month.values():
        input+=transaction_list

    left_out, MI_TRANSACTIONS = filter_medium_income_words(input, medium_income_word_list)

    avg_by_month = dict()

    for date in dateList:
        for transaction in MI_TRANSACTIONS:
            if int("".join(transaction["date"].split("-")[:2])) == date:
                try:
                    avg_by_month[date].append(transaction)
                except:
                    avg_by_month[date] = [transaction]

    avg_by_month_2 = avg_by_month.copy()

    for k in avg_by_month_2.keys():
        avg_by_month[k] = sum(avg_by_month_2[k])

    monthly_average = sum([x for x in avg_by_month.values()]) / considered_window

    valid_income_months_counter = 0
    plus_10 = monthly_average * 1.1
    minus_10 = monthly_average * 0.9

    for k in avg_by_month.keys():
        if minus_10 <= avg_by_month[k] < plus_10:
            valid_income_months_counter += 1
        else:
            avg_by_month[k] = 0

    if valid_income_months_counter == 6:
        return round(monthly_average), True
    elif valid_income_months_counter == 5:
        return round((sum(avg_by_month.values()) / 5) * 0.8), True
    else:
        return 0, False

def get_transactions_by_month(transaction_list):

    transactions_by_month = {}

    timelist = []
    for transaction in transaction_list:
        date = int("".join(transaction["date"].split("-")[:2]))

        if date not in timelist:
            timelist.append(date)

    timelist.sort()
    timelist = complete_date_list(timelist)

    for date in timelist:
        transactions_by_month[str(date)] = []

    for transaction in transaction_list:

        date = int("".join(transaction["date"].split("-")[:2]))
        transactions_by_month[str(date)].append(transaction)

    return [transactions_by_month, timelist]
