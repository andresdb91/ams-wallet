from flask import request, Response
from decimal import Decimal
import json


def init(flask_app):

    # Queries
    @flask_app.route('/v1/wallet/<user_id>/active',
                     methods=['GET'])
    def get_wallet_status(user_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<user_id>/balance',
                     methods=['GET'])
    def get_wallet_balance(user_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<user_id>/check/<amount>',
                     methods=['GET'])
    def check_wallet_for_amount(user_id: int, amount: Decimal) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<user_id>/transactions',
                     methods=['GET'])
    def get_wallet_recent_transactions(user_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<user_id>/alltransactions',
                     methods=['GET'])
    def get_wallet_all_transactions(user_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/transaction/<transaction_id>',
                     methods=['GET'])
    def check_transaction_status(transaction_id: int) -> Response:
        result = None
        return json.dumps(result)

    # Commands
    @flask_app.route('/v1/wallet/<user_id>/active',
                     methods=['POST'])
    def modify_wallet_status(user_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/transaction',
                     methods=['POST'])
    def create_transaction() -> Response:
        result = None
        return json.dumps(result)
