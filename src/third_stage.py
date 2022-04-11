
def is_recurrent(transaction_list, recurrent_window):

    final_list = transaction_list[:]
    MI_TRANSACTIONS = []

    transactions_by_month = {}
    transaction_descriptions_by_month = {}

    timelist = []
    for transaction in transaction_list:
        date = int("".join(transaction["date"].split("-")[:2]))

        if date not in timelist:
            timelist.append(date)

        try:
            transactions_by_month[str(date)].append(transaction)
            transaction_descriptions_by_month[str(date)].append(transaction["description"])
        except:
            transactions_by_month[str(date)] = [transaction]
            transaction_descriptions_by_month[str(date)] = [transaction["description"]]

    timelist.sort()

    if len(timelist) <= recurrent_window:
        return final_list, []

    for window_iterator in range(len(timelist) - recurrent_window):
        for transaction in transactions_by_month[str(timelist[window_iterator])]:
            cond = set([transaction["description"] in transaction_descriptions_by_month[str(timelist[window_iterator + element_iterator])] for element_iterator in range(recurrent_window)])

            if list(cond) == [True]:
                if transaction not in MI_TRANSACTIONS:
                    MI_TRANSACTIONS += [x for x in final_list if x['description'] == transaction['description']]
                    final_list = [x for x in final_list if x['description'] != transaction['description']]

    return final_list, MI_TRANSACTIONS