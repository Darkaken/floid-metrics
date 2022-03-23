
def has_income(HI_transaction_list, MI_transaction_list, income_window, last_considered_month):

    transaction_list = HI_transaction_list + MI_transaction_list
    timelist = []

    for transaction in transaction_list:
        date = int("".join(transaction["date"].split("-")[:2]))

        if date not in timelist:
            timelist.append(date)

    timelist = timelist.sort()[:len(timelist) - last_considered_month]

    if timelist[-income_window:-1] == complete_date_list(timelist[-income_window:-1]):
        return True
    return False

def complete_date_list(timeList):

    final_list = []

    start_year = int(str(timeList[0])[:4])
    start_month = int(str(timeList[0])[4:6])

    while True:
        if len(str(start_month)) == 1:
            iterator = int(str(start_year) + '0' + str(start_month))
        else:
            iterator = int(str(start_year) + str(start_month))

        final_list.append(iterator)

        if iterator == timeList[-1]:
            break

        start_month += 1

        if start_month == 13:
            start_month = 1
            start_year += 1

    return final_list
