
from flask import Flask, request
from flask_restful import Resource, Api
import json, time
import math
import re
import json

app = Flask(__name__)
api = Api(app)
port = 5100

high_income_words = ["ingreso", "remuneracion", "sueldo", "trabajo"]
low_income_words = ["spa", "deposito", "efectivo", "sociedad", "fundacion", "ingenieria", "transportes"]
investment_words = ["ahorro", "inversion", "fintual", "fondos", "mutuos", "rescate", "acciones"]
not_income_words = ['diez', 'modelo', 'porciento', "afp", "compra", "superoferta"]
beneficios_words = ['ife', 'solidario']

@app.route('/get_income', methods=['POST'])
def get_income():

    json_data = request.json

    results = income_test(json_data)

    json_data["income"]["income_test_data"] = {

        "high_confidence_income" : results[0],
        "low_confidence_income" : results[1],
        "no_confidence_income" : results[2],
        "ife_income" : results[3]
    }

    return json_data


def find_length(report):

    maximum = 0

    for account in report['income']['accounts']:
        if len(account['incomeByMonth']) > maximum:
            maximum = len(account['incomeByMonth'])

    return maximum


def getAllTransactions(report):

    allTransactions = []

    for account in report['transactions']['accounts']:
        try:
            for transaction in account['transactions']:
                allTransactions.append(transaction)
        except Exception as e:
            print(e)

    return allTransactions

def filter_not_words(transaction_list):

    lista = transaction_list[:]

    not_words = investment_words + not_income_words
    for transaction in transaction_list:
        for keyword in not_words:
            if keyword in transaction['description'].lower():
                try:
                    lista.remove(transaction)
                except:
                    pass

    return lista

def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def recurrentTransactions(transaction_list):

    transactions_by_month = {}
    transaction_descriptions_by_month = {}
    recurrent_transactions = []

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

    for iterator in range(len(timelist) - 3):
        for transaction in transactions_by_month[str(timelist[iterator])]:

            cond1 = transaction["description"] in transaction_descriptions_by_month[str(timelist[iterator + 1])]
            cond2 = transaction["description"] in transaction_descriptions_by_month[str(timelist[iterator + 2])]

            try:
                cond3 = transaction["description"] in transaction_descriptions_by_month[str(timelist[iterator - 1])]
            except:
                cond3 = False

            try:
                cond4 = transaction["description"] in transaction_descriptions_by_month[str(timelist[iterator - 2])]
            except:
                cond4 = False

            if cond1 and cond2:
                recurrent_transactions.append(transaction["description"])

            elif cond1 and cond3:
                recurrent_transactions.append(transaction["description"])

            elif cond3 and cond4:
                recurrent_transactions.append(transaction["description"])

    return list(set(recurrent_transactions))

def encontrar_ingreso(transaction_list, N, len_burnout):

    valor_min = N

    high_income_transactions = []
    low_income_transactions = []
    income_transactions = []
    ife_transactions = []

    not_income_transactions = []

    for transaction in transaction_list:
        try:
            if transaction['in'] >= valor_min:
                income_transactions.append(transaction)
        except:
            pass

    for transaction in income_transactions:

        desc = transaction['description'].lower()

        if len(re.sub("[^0-9]", "", desc)) >= 7:
            high_income_transactions.append(transaction)
        else:

            found = False

            for keyword in beneficios_words:
                if keyword in desc:
                    ife_transactions.append(transaction)
                    found = True
                    break

            if found:
                continue

            for keyword in high_income_words:
                if keyword in desc:
                    high_income_transactions.append(transaction)
                    found = True

            if found:
                continue

            for keyword in low_income_words:
                if keyword in desc:
                    low_income_transactions.append(transaction)
                    found = True

            if found:
                continue

            not_income_transactions.append(transaction)

    not_income_transactions_filtered = not_income_transactions[:]

    high_income_transactions = filter_not_words(high_income_transactions)
    low_income_transactions = filter_not_words(low_income_transactions)
    not_income_transactions_filtered = filter_not_words(not_income_transactions_filtered)

    recurrent_descriptions = recurrentTransactions(not_income_transactions_filtered)

    for transaction in not_income_transactions_filtered[:]:
        if transaction["description"] in recurrent_descriptions:
            low_income_transactions.append(transaction)
            not_income_transactions_filtered.remove(transaction)

    high_confidence_income = sum(transaction['in'] for transaction in high_income_transactions) / len_burnout
    low_confidence_income = sum(transaction["in"] for transaction in low_income_transactions) / len_burnout
    no_confidence_income = sum(transaction['in'] for transaction in not_income_transactions_filtered) / len_burnout
    ife_income = sum(transaction['in'] for transaction in ife_transactions) / len_burnout

    for transaction in high_income_transactions:
        print(f"high {transaction['description']} : {transaction['in']}")

    print("")
    for transaction in low_income_transactions:
        print(f"low {transaction['description']} : {transaction['in']}")

    print("")
    for transaction in not_income_transactions_filtered:
        print(f"none {transaction['description']} : {transaction['in']} : {transaction['date']}")

    print("")

    for transaction in ife_transactions:
        print(f"ife {transaction['description']} : {transaction['in']}")

    print(f' High Confidence: {round(high_confidence_income)}')
    print(f' Low Confidence: {round(low_confidence_income)}')
    print(f' Total Income: {round(float(high_confidence_income) + float(low_confidence_income))}')

    print("")
    print(f' No Confidence: {round(no_confidence_income)}')
    print(f" IFE: {round(ife_income)}")


    return [round(high_confidence_income), round(low_confidence_income), round(no_confidence_income), round(ife_income)]

def income_test(report):

        result = encontrar_ingreso(getAllTransactions(report), 25000, find_length(report))
        return result

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)