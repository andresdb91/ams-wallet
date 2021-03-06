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
    auth_url = ':'.join([host, str(port)])

    response = requests.get('/'.join(['http:/', auth_url, 'v1/users/current']),
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


def validate_owner(token, wallet_id):

    profile = validate_token(token)

    if 'id' not in profile or wallet_id != profile['id']:
        raise errors.InvalidAccessLevel()


def validate_owner_or_admin_role(token, wallet_id):
    try:
        validate_owner(token, wallet_id)
    except errors.InvalidAccessLevel:
        validate_admin_role(token)


def validate_party(token, transaction):

    profile = validate_token(token)

    if ('id' not in profile
            or profile['id'] not in [transaction.get('_id_orig'),
                                     transaction.get('_id_dest')]):
        raise errors.InvalidAccessLevel()


def invalidate_session(token):

    if isinstance(token, str) and validate_token.exists((token, )):
        validate_token.delete((token, ))
