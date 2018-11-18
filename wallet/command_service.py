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

    src_id = params.get('_id_orig')
    dst_id = params.get('_id_dest')
    amount = params.get('amount')
    tr_type = params.get('type')

    wallet_src = Wallet.objects(user_id=src_id)
    if not wallet_src:
        raise errors.InvalidArgument(src_id)

    wallet_dst = (Wallet.objects(user_id=dst_id)
                  or Wallet(user_id=dst_id, status='activa'))

    if not amount:
        raise errors.InvalidArgument(amount)

    if not tr_type or tr_type not in [
            'carga', 'debito', 'transferencia', 'consolidacion']:
        raise errors.InvalidArgument(tr_type)

    transaction = Transaction(
        wallet_src=wallet_src,
        wallet_dst=wallet_dst,
        transaction_type=tr_type,
        amount=amount)

    transaction.save()
