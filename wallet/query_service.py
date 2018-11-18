from datetime import datetime
from decimal import Decimal

from utils.security import errors

from wallet.documents import Transaction, Wallet


def get_wallet_status(user_id):
    wallet = Wallet.objects(user_id=user_id).first()

    if not wallet:
        return {
            '_id': None,
            'estado': 'not found',
            'updated': None
        }
    else:
        return {
            '_id': str(wallet.user_id),
            'estado': wallet.status,
            'updated': wallet.status_datetime.strftime('%Y-%m-%d %H:%M:%S')
        }


def get_wallet_balance(user_id):
    wallet = Wallet.objects(user_id=user_id).first()

    if not wallet:
        return {
            '_id': user_id,
            'balance': Decimal('0.00'),
            'id_last_trans': None,
            'dt_last_trans': None,
            'id_last_cons': None,
            'dt_last_cons': None
        }

    cons_id, cons_date, cons_balance = get_last_consolidation_info(wallet)
    balance, last_transaction = get_balance(wallet, cons_date, cons_balance)

    return {
        '_id': wallet.user_id,
        'balance': str(balance),
        'id_last_trans': str(last_transaction._id),
        'dt_last_trans': last_transaction.transaction_dt
            .strftime('%Y-%m-%d %H:%M:%S'),
        'id_last_cons': str(cons_id),
        'dt_last_cons': cons_date.strftime('%Y-%m-%d')
    }


def check_available_amount(user_id, amount):
    wallet = Wallet.objects(user_id=user_id).first()

    if not wallet:
        return {
            '_id': user_id,
            'amount_check': False
        }

    _, cons_date, cons_balance = get_last_consolidation_info(wallet)
    balance, _ = get_balance(wallet, cons_date, cons_balance)

    if amount <= balance:
        check = True
    else:
        check = False

    return {
        '_id': str(wallet.user_id),
        'amount_check': check
    }


def get_wallet_recent_transactions(user_id):
    wallet = Wallet.objects(user_id=user_id).first()

    if not wallet:
        return [{}]

    _, cons_date, _ = get_last_consolidation_info(wallet)

    debitos = Transaction.objects(
        wallet_src=wallet.user_id,
        transaction_dt__gt=cons_date,
        transaction_type='debito'
    ).all()
    transf_out = Transaction.objects(
        wallet_src=wallet.user_id,
        transaction_dt__gt=cons_date,
        transaction_type='transferencia'
    ).all()
    transaction_out = list(debitos) + list(transf_out)

    cargas = Transaction.objects(
        wallet_dst=wallet.user_id,
        transaction_dt__gt=cons_date,
        transaction_type='carga'
    ).all()
    transf_in = Transaction.objects(
        wallet_dst=wallet.user_id,
        transaction_dt__gt=cons_date,
        transaction_type='transferencia'
    ).all()
    transaction_in = list(cargas) + list(transf_in)

    transactions = []
    for tr in transaction_in:
        transactions.append({
            '_id': str(tr._id),
            'created': tr.transaction_dt.strftime('%Y-%m-%d %H:%M:%S'),
            '_id_orig': str(tr.wallet_src),
            '_id_dest': str(tr.wallet_dst),
            'amount': str(tr.amount),
            'type': tr.transaction_type
        })
    for tr in transaction_out:
        transactions.append({
            '_id': str(tr._id),
            'created': tr.transaction_dt.strftime('%Y-%m-%d %H:%M:%S'),
            '_id_orig': str(tr.wallet_src),
            '_id_dest': str(tr.wallet_dst),
            'amount': str(tr.amount),
            'type': tr.transaction_type
        })

    return transactions


def get_wallet_all_transactions(user_id):
    wallet = Wallet.objects(user_id=user_id).first()

    if not wallet:
        return [{}]

    debitos = Transaction.objects(
        wallet_src=wallet.user_id,
        transaction_type='debito'
    ).all()
    transf_out = Transaction.objects(
        wallet_src=wallet.user_id,
        transaction_type='transferencia'
    ).all()
    transaction_out = list(debitos) + list(transf_out)

    cargas = Transaction.objects(
        wallet_dst=wallet.user_id,
        transaction_type='carga'
    ).all()
    transf_in = Transaction.objects(
        wallet_dst=wallet.user_id,
        transaction_type='transferencia'
    ).all()
    transaction_in = list(cargas) + list(transf_in)

    transactions = []
    for tr in transaction_in:
        transactions.append({
            '_id': str(tr._id),
            'created': tr.transaction_dt.strftime('%Y-%m-%d %H:%M:%S'),
            '_id_orig': str(tr.wallet_src),
            '_id_dest': str(tr.wallet_dst),
            'amount': str(tr.amount),
            'type': tr.transaction_type
        })
    for tr in transaction_out:
        transactions.append({
            '_id': str(tr._id),
            'created': tr.transaction_dt.strftime('%Y-%m-%d %H:%M:%S'),
            '_id_orig': str(tr.wallet_src),
            '_id_dest': str(tr.wallet_dst),
            'amount': str(tr.amount),
            'type': tr.transaction_type
        })

    return transactions


def get_transaction(transaction_id):
    transaction = Transaction.objects(transaction_id=transaction_id).first()

    if not transaction:
        raise errors.InvalidArgument(transaction_id)

    return {
        '_id': str(transaction._id),
        'created': transaction.transaction_dt.strftime('%Y-%m-%d %H:%M:%S'),
        ' _id_orig': str(transaction.wallet_src),
        ' _id_dest': str(transaction.wallet_dst),
        'amount': str(transaction.amount),
        'type': transaction.transaction_type
    }


def get_balance(wallet, cons_date, cons_balance):

    debitos = Transaction.objects(
        wallet_src=wallet.user_id,
        transaction_dt__gt=cons_date,
        transaction_type='debito'
    ).all()
    transf_out = Transaction.objects(
        wallet_src=wallet.user_id,
        transaction_dt__gt=cons_date,
        transaction_type='transferencia'
    ).all()
    transaction_out = list(debitos) + list(transf_out)

    cargas = Transaction.objects(
        wallet_dst=wallet.user_id,
        transaction_dt__gt=cons_date,
        transaction_type='carga'
    ).all()
    transf_in = Transaction.objects(
        wallet_dst=wallet.user_id,
        transaction_dt__gt=cons_date,
        transaction_type='transferencia'
    ).all()
    transaction_in = list(cargas) + list(transf_in)

    balance = cons_balance

    last_transaction = None

    for tr_out in transaction_out:
        balance -= tr_out.amount
        if (last_transaction
                and last_transaction.transaction_dt < tr_out.transaction_dt):
            last_transaction = tr_out

    for tr_in in transaction_in:
        balance += tr_in.amount
        if (last_transaction
                and last_transaction.transaction_dt < tr_in.transaction_dt):
            last_transaction = tr_in

    return balance, last_transaction


def get_last_consolidation_info(wallet):

    consolidation = Transaction.objects(
        wallet_dst=wallet.user_id,
        transaction_type='consolidacion'
    ).order_by('-transaction_dt').first()

    if consolidation:
        cons_date = consolidation.transaction_dt
        cons_id = consolidation._id
        cons_balance = consolidation.amount
    else:
        cons_date = datetime.min
        cons_id = None
        cons_balance = Decimal('0.00')

    return cons_id, cons_date, cons_balance
