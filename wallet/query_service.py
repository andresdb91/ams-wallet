from datetime import datetime
from decimal import Decimal

from utils.security import errors

from wallet.documents import Transaction, Wallet


def get_wallet_status(user_id):
    wallet = Wallet.objects(user_id=user_id).limit(1)

    if not wallet:
        return {
            '_id': None,
            'estado': 'not found',
            'updated': None
        }
    else:
        return {
            '_id': wallet.user_id,
            'estado': wallet.status,
            'updated': wallet.status_datetime
        }


def get_wallet_balance(user_id):
    wallet = Wallet.objects(user_id=user_id).limit(1)

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
        'balance': balance,
        'id_last_trans': last_transaction.transaction_id,
        'dt_last_trans': last_transaction.transaction_dt,
        'id_last_cons': cons_id,
        'dt_last_cons': cons_date
    }


def check_available_amount(user_id, amount):
    pass


def get_wallet_recent_transactions(user_id):
    pass


def get_wallet_all_transactions(user_id):
    pass


def get_transaction(transaction_id):
    pass


def get_balance(wallet, cons_date, cons_balance):

    transactions_from = Transaction.objects(
        wallet_src=wallet,
        transaction_dt__gt=cons_date
    ).all()
    transactions_to = Transaction.objects(
        wallet_dst=wallet,
        transaction_type='debito',
        transaction_dt__gt=cons_date
    ).all()

    balance = cons_balance

    last_transaction = None

    for tr_out in transactions_from:
        balance -= tr_out.amount
        if (last_transaction
                and last_transaction.transaction_dt < tr_out.transaction_dt):
            last_transaction = tr_out

    for tr_in in transactions_to:
        balance += tr_in.amount
        if (last_transaction
                and last_transaction.transaction_dt < tr_in.transaction_dt):
            last_transaction = tr_in

    return balance, last_transaction


def get_last_consolidation_info(wallet):

    consolidation = Transaction.objects(
        wallet_dst=wallet,
        transaction_type='consolidacion'
    ).order_by('-transaction_dt').first()

    if consolidation:
        cons_date = consolidation.transaction_dt
        cons_id = consolidation.transaction_id
        cons_balance = consolidation.amount
    else:
        cons_date = datetime.min
        cons_id = None
        cons_balance = Decimal('0.00')

    return cons_id, cons_date, cons_balance
