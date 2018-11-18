from utils.security import errors

from wallet.documents import Transaction, Wallet


def get_wallet_status(user_id):
    wallet = Wallet.objects(user_id=user_id) or Wallet(user_id=user_id,
                                                       estado='active')

    wallet.save()

    return {
        '_id': wallet.user_id,
        'estado': wallet.status,
        'updated': wallet.status_datetime
    }


def get_wallet_balance(user_id):
    pass


def check_available_amount(user_id, amount):
    pass


def get_wallet_recent_transactions(user_id):
    pass


def get_wallet_all_transactions(user_id):
    pass


def get_transaction(transaction_id):
    pass
