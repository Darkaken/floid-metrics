
def filter_not_words(transaction_list, not_income_word_list):

    final_list = transaction_list[:]

    for transaction in transaction_list:
        for keyword in not_income_word_list:
            if keyword in transaction['description'].lower():
                try:
                    final_list.remove(transaction)
                except:
                    pass

    return final_list