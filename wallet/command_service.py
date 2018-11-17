from datetime import datetime
from utils.security import errors

from wallet.documents import Transaction, Wallet


def update_status(user_id, params):

    wallet = Wallet.objects(user_id=int(user_id))

    if not wallet:
        wallet = Wallet(user_id=user_id, status='activa')

    estado = params.get('estado')
    if estado and estado in ['activa', 'suspendida', 'cerrada']:
        wallet.status = estado
        wallet.status_datetime = datetime.now()
        wallet.save()
    else:
        raise errors.InvalidArgument(params)


def create_transaction(params):
    pass
