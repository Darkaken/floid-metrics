
from datetime import date

class ErrorLog(object):

    log_counter = 0

    def __init__(self, exception, json_data):

        ErrorLog.log_counter += 1

        self.date = date.today()
        self.exception = exception
        self.report = json_data

