
def metrics(list_after_third_stage, MI_TRANSACTIONS, HI_TRANSACTIONS, total_time_months, all_transactions):

    result = {

        'monthly_high_confidence_income' : round(sum([x['in'] for x in HI_TRANSACTIONS]) / total_time_months),
        'monthly_medium_confidence_income' : round(sum([x['in'] for x in MI_TRANSACTIONS]) / total_time_months),
        'monthly_no_confidence_income' : not_income_metrics(all_transactions, MI_TRANSACTIONS, HI_TRANSACTIONS, total_time_months)

    }

    return result

def not_income_metrics(all_transactions, MI_TRANSACTIONS, HI_TRANSACTIONS, total_time_months):

    income_transactions = MI_TRANSACTIONS + HI_TRANSACTIONS

    return round(sum([transaction for transaction in all_transactions if (transaction['in'] > 0 and transaction not in income_transactions)]) / total_time_months)