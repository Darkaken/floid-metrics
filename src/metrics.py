
def metrics(list_after_third_stage, MI_TRANSACTIONS, HI_TRANSACTIONS, total_time_months):

    result = {

        'monthly_high_confidence_income' : round(sum([x['in'] for x in HI_TRANSACTIONS]) / total_time_months),
        'monthly_medium_confidence_income' : round(sum([x['in'] for x in MI_TRANSACTIONS]) / total_time_months),
        'monthly_no_confidence_income' : round(sum([x['in'] for x in list_after_third_stage]) / total_time_months),
    }

    result['income_total'] = result["monthly_high_confidence_income"] + result["monthly_medium_confidence_income"]

    return result