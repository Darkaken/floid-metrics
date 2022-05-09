
def over_minimum_quantity(transaction_list, minimum_ammount):

    return_transaction_list = []

    transaction_list = [x for x in transaction_list if x["in"] > 0]

    transactions_by_month = {}

    for transaction in transaction_list:
        date = int("".join(transaction["date"].split("-")[:2]))

        try:
            transactions_by_month[str(date)].append(transaction)
        except:
            transactions_by_month[str(date)] = [transaction]

    for key, value in transactions_by_month.items():

        desc_counter = {}

        for transaction in value:
            try:
                desc_counter[transaction["description"]].append(transaction)
            except:
                desc_counter[transaction["description"]] = [transaction]

        to_consider = [value for key, value in desc_counter.items() if sum([transaction["in"] for transaction in value]) >= minimum_ammount]

        if to_consider:
            return_transaction_list += [item for sublist in to_consider for item in sublist]

    print(return_transaction_list)

    return return_transaction_list