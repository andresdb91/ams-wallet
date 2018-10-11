from mongoengine import *

connect('ecommerce-wallet', host='localhost', port=27017)


class Wallet(Document):
    # wallet_id
    # user_id
    # balance
    # balance_datetime
    # status
    # status_datetime
    pass


class Transaction(Document):
    # transaction_id
    # transaction_type
    # wallet_src
    # wallet_dst
    # amount
    # status
    # status_datetime
    pass


class ServiceStatus(Document):
    # status
    # status_datetime
    pass
