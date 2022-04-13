
class Parameters(object):

    possible_parameters = [
        'monto_minimo_tranzado',
        'not_income_words',
        'high_income_words',
        'medium_income_words',
        'rut_minimo',
        'consecutividad',
    ]

    def __init__(self, json_parameters):

        self.params_ammount = 0

        for key, value in json_parameters.items():

            if key not in Parameters.possible_parameters:
                raise WrongParameterNameError

            else:
                exec(f'self.{key} = {value}')
                self.params_ammount += 1

        self.check_integrity()

    def check_integrity(self):

        if self.params_ammount != 8:
            raise WrongParameterAmmountError


class WrongParameterNameError(Exception):
    def __str__(self):
        return 'WrongParameterNameError'

class WrongParameterAmmountError(Exception):
    def __str__(self):
        return 'WrongParameterAmmountError'