import traceback
import json


class InvalidRequest(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class InvalidArgument(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class MultipleArgumentException(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class InvalidAuth(Exception):
    pass


class InvalidAccessLevel(Exception):
    pass


def handle_error(err):
    if isinstance(err, InvalidArgument):
        return handle_invalid_argument(err)
    elif isinstance(err, InvalidAuth):
        return handle_invalid_auth(err)
    elif isinstance(err, InvalidAccessLevel):
        return handle_invalid_access_level(err)
    else:
        traceback.print_exc()
        return handle_unknown(err)


def handle_invalid_argument(err):
    return json.dumps({'error': 'Argumento inválido'}), 400


def handle_invalid_auth(err):
    return json.dumps({'error': 'No autorizado'}), 401


def handle_invalid_access_level(err):
    return json.dumps({'error': 'No tiene permisos suficientes'}), 401


def handle_unknown(err):
    return json.dumps({'error': 'Error desconocido'}), 500
