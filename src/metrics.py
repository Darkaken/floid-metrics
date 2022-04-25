
def metrics(list_after_third_stage, MI_TRANSACTIONS, HI_TRANSACTIONS, total_time_months):

    main_income = MI_TRANSACTIONS + HI_TRANSACTIONS
    income_months = different_month_ammount(main_income)

    result = {

        'regularity': f"{income_months}/{total_time_months}",
        'mainAverage' : round(sum([x['in'] for x in main_income]) / total_time_months),
        'extraAverage' : round(sum([x['in'] for x in list_after_third_stage]) / total_time_months),
        'mainIncomeDeposit': main_income_deposit(main_income),
    }

    print(income_by_month(result, main_income, list_after_third_stage))
    result['incomeByMonth']: income_by_month(result, main_income, list_after_third_stage)

    return result

def different_month_ammount(transaction_list):

    observed_months = []

    for transaction in transaction_list:

        if int("".join(transaction["date"].split("-")[:2])) not in observed_months:
            observed_months.append(int("".join(transaction["date"].split("-")[:2])))

    return len(observed_months)

def main_income_deposit(transaction_list):

    if not transaction_list:
        return None

    description_counter = dict()

    for transaction in transaction_list:

        try:
            description_counter[transaction['description']] += 1
        except:
            description_counter[transaction['description']] = 1

    return [key for key, value in description_counter.items() if value == max([value for value in description_counter.values()])][0]

def income_by_month(result, main_income, extra_income):

    transactions_by_month = {}
    result["incomeByMonth"] = []

    for transaction in main_income:
        date = int("".join(transaction["date"].split("-")[:2]))

        try:
            transactions_by_month[str(date)].append(transaction)
        except:
            transactions_by_month[str(date)] = [transaction]

    for date, value in transactions_by_month.items():

        result['incomeByMonth'].append({
            'month': f'{str(date)[:4]}-{str(date[4:])}',
            'main': round(sum(transaction['in'] for transaction in value)),
            'extra': 0,
            'sources': [expand_transaction(transaction, 'main') for transaction in value]
        })

    extra_by_month = {}

    for transaction in extra_income:
        date = int("".join(transaction["date"].split("-")[:2]))

        if date == 202201:
            print(transaction)

        try:
            extra_by_month[str(date)] += transaction["in"]
        except:
            extra_by_month[str(date)] = transaction["in"]

    for bundle in result["incomeByMonth"]:
        for date, value in extra_by_month.items():
            if f'{str(date)[:4]}-{str(date[4:])}' == bundle["month"]:
                bundle["extra"] = value

    return result


def expand_transaction(transaction, types):

    return {
        'sender': transaction['description'],
        'amount': transaction['in'],
        'type': types
    }
