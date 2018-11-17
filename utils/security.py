from memoize import Memoizer
import requests
import utils.errors as errors
from utils import config

memoKeys = {}
memo = Memoizer(memoKeys)


@memo(max_age=3600)
def validate_token(token):

    if not isinstance(token, str) or len(token) == 0:
        raise errors.InvalidAuth()

    headers = {'Authorization'.encode(): token.encode()}

    host = config.get_auth_server_url()
    port = config.get_auth_server_port()
    auth_url = ':'.join([host, port])

    response = requests.get('/'.join([auth_url, '/v1/users/current']),
                            headers=headers)

    if response.status_code != 200:
        raise errors.InvalidAuth()

    result = response.json()
    if not result:
        raise errors.InvalidAuth()

    return result


def validate_admin_role(token):

    profile = validate_token(token)

    if 'permissions' not in profile or 'admin' not in profile['permissions']:
        raise errors.InvalidAccessLevel()


def validate_owner(token, wallet):

    profile = validate_token(token)

    if 'id' not in profile or wallet.id != profile['id']:
        raise errors.InvalidAccessLevel()


def invalidate_session(token):

    if isinstance(token, str) and validate_token.exists((token, )):
        validate_token.delete((token, ))
