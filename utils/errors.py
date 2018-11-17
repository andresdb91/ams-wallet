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
    # def __init__(self, error):
    #     self.error = error
    #
    # def __str__(self):
    #     return repr(self.error)
    pass


class InvalidAccessLevel(Exception):
    # def __init__(self, error):
    #     self.error = error
    #
    # def __str__(self):
    #     return repr(self.error)
    pass


def handle_error(err):
    if isinstance(err, InvalidRequest):
        return handle_invalid_request(err)
    elif isinstance(err, InvalidArgument):
        return handle_invalid_argument(err)
    elif isinstance(err, MultipleArgumentException):
        return handle_multiple_argument_exception(err)
    elif isinstance(err, InvalidAuth):
        return handle_invalid_auth(err)
    elif isinstance(err, InvalidAccessLevel):
        return handle_invalid_access_level(err)
    else:
        traceback.print_exc()
        return handle_unknown(err)


def handle_invalid_request(err):
    pass


def handle_invalid_argument(err):
    pass


def handle_multiple_argument_exception(err):
    pass


def handle_invalid_auth(err):
    pass


def handle_invalid_access_level(err):
    pass


def handle_unknown(err):
    pass
