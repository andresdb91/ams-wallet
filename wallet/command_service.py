from datetime import datetime
from utils.security import errors

from wallet.documents import Transaction, Wallet


def update_status(user_id, params):

    wallet = Wallet.objects(user_id=int(user_id)).limit(1)

    if not wallet:
        wallet = Wallet(user_id=user_id, status='activa')

    estado = params.get('estado')
    if estado and estado in ['activa', 'suspendida', 'cerrada']:
        wallet.status = estado
        wallet.status_datetime = datetime.now()
        wallet.save()
    else:
        raise errors.InvalidArgument(params)

    wallet.save()

    return {
        '_id': wallet.user_id,
        'estado': wallet.status
    }


def create_transaction(params):

    src_id = params.get('_id_orig')
    dst_id = params.get('_id_dest')
    amount = params.get('amount')
    tr_type = params.get('type')

    wallet_src = Wallet.objects(user_id=src_id).limit(1)
    wallet_dst = (Wallet.objects(user_id=dst_id).limit(1)
                  or Wallet(user_id=dst_id, status='activa'))

    if tr_type == 'carga':
        if not amount:
            raise errors.InvalidArgument(amount)
        transaction = Transaction(
            wallet_dst=wallet_dst,
            transaction_type=tr_type,
            amount=amount)
    elif tr_type == 'debito':
        if not amount:
            raise errors.InvalidArgument(amount)
        if not wallet_src:
            raise errors.InvalidArgument(src_id)
        transaction = Transaction(
            wallet_src=wallet_src,
            transaction_type=tr_type,
            amount=amount)
    elif tr_type == 'transferencia':
        if not amount:
            raise errors.InvalidArgument(amount)
        if not wallet_src:
            raise errors.InvalidArgument(src_id)
        transaction = Transaction(
            wallet_src=wallet_src,
            wallet_dst=wallet_dst,
            transaction_type=tr_type,
            amount=amount)
    elif tr_type == 'consolidacion':
        if not amount:
            raise errors.InvalidArgument(amount)
        transaction = Transaction(
            wallet_dst=wallet_dst,
            transaction_type=tr_type,
            amount=amount)
    else:
        raise errors.InvalidArgument(tr_type)

    transaction.save()
    wallet_dst.save()

    return {
        '_id': transaction.transaction_id,
        'created': transaction.transaction_dt,
        '_id_orig': transaction.wallet_src,
        '_id_dest': transaction.wallet_dst,
        'amount': transaction.amount,
        'type': transaction.transaction_type
    }
