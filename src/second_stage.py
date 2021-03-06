
import re

def filter_high_income_words(transaction_list, high_income_word_list):

    final_list = transaction_list[:]
    HI_TRANSACTIONS = []

    for transaction in transaction_list:
        for keyword in high_income_word_list:
            if keyword in transaction['description'].lower():
                try:
                    final_list.remove(transaction)
                    HI_TRANSACTIONS.append(transaction)
                except:
                    pass

    return final_list, HI_TRANSACTIONS

def filter_medium_income_words(transaction_list, medium_income_word_list):

    final_list = transaction_list[:]
    MI_TRANSACTIONS = []

    for transaction in transaction_list:
        for keyword in medium_income_word_list:
            if keyword in transaction['description'].lower():
                try:
                    final_list.remove(transaction)
                    MI_TRANSACTIONS.append(transaction)
                except:
                    pass

    return final_list, MI_TRANSACTIONS

def RUT_analysis(transaction_list, minimum_rut):

    final_list = transaction_list[:]
    RUT_TRANSACTIONS = []

    for transaction in transaction_list:
        transaction_description_list = transaction['description'].lower().split(' ')

        for substring in transaction_description_list:
            number = filter_zero(re.sub("[^0-9]", "", substring.lower()))

            if len(number) == 8 or len(number) == 9:
                if int(number[:8]) >= minimum_rut:
                    if not digito_verificador(number[:8]):

                        if "/" not in substring:
                            try:
                                final_list.remove(transaction)
                                RUT_TRANSACTIONS.append(transaction)
                            except:
                                pass

    return final_list, RUT_TRANSACTIONS

def filter_zero(rut):

    final = ""
    digit_found = False

    for char in rut:
        if char == "0":
            if digit_found:
                final += char
            else:
                pass
        else:
            digit_found = True
            final += char

    return final

def digito_verificador(rut):

    rut = str(rut)
    digito = rut[-1]

    multiplication_vector = [2, 3, 4, 5, 6, 7, 2, 3]
    total = 0

    rut = rut[:-1][::-1]

    for i in range(len(rut)):
        total += int(rut[i]) * multiplication_vector[i]

    verificador = 11 - (total - (total//11 * 11))

    if verificador == 11:
        verificador = 0

    if verificador == int(digito):
        return True
    return False

