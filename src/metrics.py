
def metrics(list_after_third_stage, MI_TRANSACTIONS, HI_TRANSACTIONS, total_time_months):

    result = {

        'high_confidence_income' : sum([x['in'] for x in list_after_third_stage]) / total_time_months,
        'medium_confidence_income' : sum([x['in'] for x in MI_TRANSACTIONS]) / total_time_months,
        'no_confidence_income' : sum([x['in'] for x in HI_TRANSACTIONS]) / total_time_months,

    }

    return result