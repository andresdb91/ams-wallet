from datetime import datetime
from decimal import Decimal

from utils.security import errors
from wallet.documents import Transaction, Wallet


def update_status(user_id, params):

    wallet = Wallet.objects(user_id=user_id).first()

    if not wallet:
        wallet = Wallet(user_id=user_id, status='activa')

    rol = params.get('role')

    estado = params.get('estado')
    if estado and (
            estado in ['activa', 'suspendida']
            or (estado and estado == 'cerrada' and rol == 'admin')):
        wallet.status = estado
        wallet.status_datetime = datetime.now()
        wallet.save()
    else:
        raise errors.InvalidArgument(params)

    return {
        '_id': str(wallet.user_id),
        'estado': wallet.status
    }


def create_transaction(params):

    src_id = params.get('_id_orig')
    dst_id = params.get('_id_dest')
    amount = params.get('amount')
    tr_type = params.get('type')

    if src_id:
        wallet_src = Wallet.objects(user_id=src_id).first()
    else:
        wallet_src = None

    if dst_id:
        wallet_dst = (Wallet.objects(user_id=dst_id).first()
                      or Wallet(user_id=dst_id, status='activa'))
    else:
        wallet_dst = None

    if not amount:
        raise errors.InvalidArgument(amount)
    else:
        amount = Decimal(amount)

    if tr_type == 'carga':
        transaction = Transaction(
            wallet_dst=wallet_dst.user_id,
            transaction_type=tr_type,
            amount=amount)
    elif tr_type == 'debito':
        if not wallet_src:
            raise errors.InvalidArgument(src_id)
        transaction = Transaction(
            wallet_src=wallet_src.user_id,
            transaction_type=tr_type,
            amount=amount)
    elif tr_type == 'transferencia':
        if not wallet_src:
            raise errors.InvalidArgument(src_id)
        transaction = Transaction(
            wallet_src=wallet_src.user_id,
            wallet_dst=wallet_dst.user_id,
            transaction_type=tr_type,
            amount=amount)
    elif tr_type == 'consolidacion':
        transaction = Transaction(
            wallet_dst=wallet_dst.user_id,
            transaction_type=tr_type,
            amount=amount)
    else:
        raise errors.InvalidArgument(tr_type)

    transaction.save()
    wallet_dst.save()

    return {
        '_id': str(transaction._id),
        'created': transaction.transaction_dt.strftime('%Y-%m-%d %H:%M:%S'),
        '_id_orig': str(transaction.wallet_src),
        '_id_dest': str(transaction.wallet_dst),
        'amount': str(transaction.amount),
        'type': transaction.transaction_type
    }
