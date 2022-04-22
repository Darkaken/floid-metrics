
import pickle

from src.ERROR_LOGGING import ErrorLog
from src.parameters_and_exceptions import *

from src.initial_filters import over_minimum_quantity
from src.first_stage import filter_not_words

from src.second_stage import filter_high_income_words
from src.second_stage import filter_medium_income_words
from src.second_stage import RUT_analysis

from src.third_stage import is_recurrent
from src.has_income import month_amount
from src.metrics import metrics

def main(json_data):

    try:

        parameter_object = Parameters(json_data['parametros'])

        initial_transaction_list = json_data["transactions"]

        if initial_transaction_list is None:
            return {
                "Error": "No hay transacciones disponibles"
            }

        total_time_months = month_amount(initial_transaction_list)

        list_after_initial_filters = over_minimum_quantity(initial_transaction_list, parameter_object.monto_minimo_tranzado)

        list_after_first_stage = filter_not_words(list_after_initial_filters, parameter_object.not_income_words)

        list_after_HI_filter, HI_TRANSACTIONS = filter_high_income_words(list_after_first_stage, parameter_object.high_income_words)

        list_after_MI_filter, MI_TRANSACTIONS = filter_medium_income_words(list_after_HI_filter, parameter_object.medium_income_words)

        list_after_RUT_filter, RUT_TRANSACTIONS = RUT_analysis(list_after_MI_filter, parameter_object.rut_minimo)

        list_after_third_stage, MI_TRANSACTIONS_2 = is_recurrent(list_after_RUT_filter, parameter_object.consecutividad)

        MI_TRANSACTIONS = MI_TRANSACTIONS + MI_TRANSACTIONS_2 + RUT_TRANSACTIONS

        result = metrics(list_after_third_stage, MI_TRANSACTIONS, HI_TRANSACTIONS, total_time_months)

        return result

    except KeyError as e:

        MSG = 'Error ha sido notificado al desarrollador y se va a solucionar en la proxima actualizacion de la API'

        if e == WrongParameterNameError:
            MSG = 'Error en la entrada de parametros'

        if e == WrongParameterAmmountError:
            MSG = 'Error en la entrada de parametros'

        else:
            log_error(e.__str__(), json_data)
            pass

        return_dict = {
            'Error': e.__str__(),
            'MSG': MSG
        }

        return return_dict

def getAllTransactions(report):

    #analisis preliminar de la estructura de un reporte

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

    file_handler = open(f'ErrorLogs/error_log_{ErrorLog.log_counter}.pickle', 'wb')
    pickle.dump(error_object, file_handler)
    file_handler.close()
