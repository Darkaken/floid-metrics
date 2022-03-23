
def over_minimum_quantity(transaction_list, minimum_ammount):
    return [transaction for transaction in transaction_list if transaction['in'] >= minimum_ammount]
