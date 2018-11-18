from mongoengine import Document
from mongoengine import fields
from mongoengine import connect
from datetime import datetime
from utils import config


def init():
    host = config.get_db_server_url()
    port = config.get_db_server_port()
    connect(
        'ecommerce-wallet',
        host=host,
        port=port
    )


class Wallet(Document):
    user_id = fields.ObjectIdField(required=True)
    status = fields.StringField(required=True)
    status_datetime = fields.DateTimeField(default=datetime.now)


class Transaction(Document):
    _id = fields.ObjectIdField(required=True, default=fields.ObjectId)
    transaction_type = fields.StringField(required=True)
    wallet_src = fields.ObjectIdField()
    wallet_dst = fields.ObjectIdField()
    amount = fields.DecimalField(required=True, force_string=True, precision=2)
    transaction_dt = fields.DateTimeField(default=datetime.now)
