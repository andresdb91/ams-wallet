from mongoengine import Document
from mongoengine import fields
from mongoengine import connect
from datetime import datetime

connect('ecommerce-wallet', host='wallet_mongodb', port=27017)


class Wallet(Document):
    user_id = fields.ObjectIdField(required=True)
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
