from flask import request, Response
from decimal import Decimal
import json


def init(flask_app):

    @flask_app.route('/v1/wallet/status', methods=['GET'])
    def check_status() -> Response:
        return Response('Status OK', 200)

    @flask_app.route('/v1/wallet/user/<user_id>', methods=['GET'])
    def get_user_wallet_id(user_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<wallet_id>/status', methods=['GET'])
    def get_wallet_status(wallet_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<wallet_id>/public', methods=['GET'])
    def get_wallet_public_info(wallet_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<wallet_id>/balance', methods=['GET'])
    def get_wallet_balance(wallet_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<wallet_id>/check/<amount>', methods=['GET'])
    def check_wallet_for_amount(wallet_id: int, amount: Decimal) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<wallet_id>/alltransactions', methods=['GET'])
    def get_wallet_all_transactions(wallet_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/<wallet_id>/transactions', methods=['GET'])
    def get_wallet_recent_transactions(wallet_id: int) -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/transaction', methods=['POST'])
    def create_transaction() -> Response:
        result = None
        return json.dumps(result)

    @flask_app.route('/v1/wallet/transaction/<transact_id>', methods=['GET'])
    def check_transaction_status(transact_id: int) -> Response:
        result = None
        return json.dumps(result)
