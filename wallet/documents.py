from mongoengine import Document
from mongoengine import fields
from mongoengine import connect
from datetime import datetime

connect('ecommerce-wallet', host='localhost', port=27017)


class Wallet(Document):
    wallet_id = fields.IntField(required=True)
    user_id = fields.IntField(required=True)
    balance = fields.DecimalField(required=True)
    balance_datetime = fields.DateTimeField(default=datetime.now)
    status = fields.StringField(required=True)
    status_datetime = fields.DateTimeField(default=datetime.now)


class Transaction(Document):
    transaction_id = fields.IntField(required=True)
    transaction_type = fields.StringField(required=True)
    wallet_src = fields.IntField()
    wallet_dst = fields.IntField()
    amount = fields.DecimalField(required=True)
    status = fields.StringField(required=True)
    status_datetime = fields.DateTimeField(default=datetime.now)


class ServiceStatus(Document):
    status = fields.StringField(required=True)
    status_datetime = fields.DateTimeField(default=datetime.now)
