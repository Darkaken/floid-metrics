
def metrics(list_after_third_stage, MI_TRANSACTIONS, HI_TRANSACTIONS, total_time_months):

    income_months = different_month_ammount(HI_TRANSACTIONS + MI_TRANSACTIONS)

    result = {

        'regularity': f"{income_months}/{total_time_months}",
        'mainAverage' : round(sum([x['in'] for x in HI_TRANSACTIONS]) / total_time_months) + round(sum([x['in'] for x in MI_TRANSACTIONS]) / total_time_months),
        'extraAverage' : round(sum([x['in'] for x in list_after_third_stage]) / total_time_months),
    }

    return result


def different_month_ammount(transaction_list):

    observed_months = []

    for transaction in transaction_list:

        if int("".join(transaction["date"].split("-")[:2])) not in observed_months:
            observed_months.append(int("".join(transaction["date"].split("-")[:2])))

    return len(observed_months)