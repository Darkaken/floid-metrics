
import pickle

from src.ERROR_LOGGING import ErrorLog
from src.parameters_and_exceptions import *

from src.initial_filters import over_minimum_quantity

from src.first_stage import filter_not_words

from src.second_stage import filter_high_income_words
from src.second_stage import filter_medium_income_words
from src.second_stage import RUT_analysis

from src.third_stage import is_recurrent

from src.has_income import has_income


def main(json_data):

    try:

        parameter_object = Parameters(json_data['parametros'])
        initial_transaction_list = getAllTransactions(json_data)

        list_after_initial_filters = over_minimum_quantity(initial_transaction_list, parameter_object.monto_minimo_tranzado)

        list_after_first_stage = filter_not_words(list_after_initial_filters, parameter_object.not_income_word_list)

        list_after_HI_filter, HI_TRANSACTIONS = filter_high_income_words(list_after_first_stage, parameter_object.high_income_word_list)

        list_after_MI_filter, MI_TRANSACTIONS = filter_medium_income_words(list_after_HI_filter, parameter_object.medium_income_words)

        list_after_RUT_filter, RUT_TRANSACTIONS = RUT_analysis(list_after_MI_filter, parameter_object.rut_minimo)

        list_after_third_stage, MI_TRANSACTIONS_2 = is_recurrent(list_after_RUT_filter, parameter_object.consecutividad)

        MI_TRANSACTIONS = MI_TRANSACTIONS + MI_TRANSACTIONS_2

        HAS_INCOME = has_income(HI_TRANSACTIONS, MI_TRANSACTIONS, parameter_object.consecutividad_ingresos, parameter_object.ultimo_mes_a_considerar)



        return json_data

    except Exception as e:

        MSG = 'Error ha sido notificado al desarrollador y se va a solucionar en la proxima actualizacion de la API'

        if e == WrongParameterNameError:
            MSG = 'Error en la entrada de parametros'

        if e == WrongParameterAmmountError:
            MSG = 'Error en la entrada de parametros'

        else:
            log_error(e.__str__(), json_data)

        return_dict = {
            'Error': e.__str__(),
            'MSG': MSG
        }

        return return_dict

def getAllTransactions(report):

    allTransactions = []

    for account in report['transactions']['accounts']:
        try:
            for transaction in account['transactions']:
                allTransactions.append(transaction)
        except Exception as e:
            print(e)

    return allTransactions

def log_error(error_msg, json_data):

    error_object = ErrorLog(error_msg, json_data)

    file_handler = open(f'error_log_{ErrorLog.log_counter}', 'wb')
    pickle.dump(error_object, file_handler)
    file_handler.close()
