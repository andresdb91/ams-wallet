from flask import request, Response
from decimal import Decimal
import json
from utils import security
from wallet import query_service, command_service
from utils.errors import handle_error


def init(flask_app):

    # Queries
    @flask_app.route('/v1/wallet/<user_id>/active',
                     methods=['GET'])
    def get_wallet_status(user_id) -> Response:
        try:
            data = query_service.get_wallet_status(user_id)
            return json.dumps(data)
        except Exception as err:
            return handle_error(err)

    @flask_app.route('/v1/wallet/<user_id>/balance',
                     methods=['GET'])
    def get_wallet_balance(user_id) -> Response:
        try:
            token = request.headers.get('Authorization')
            security.validate_owner(token, user_id)

            data = query_service.get_wallet_balance(user_id)
            return json.dumps(data)
        except Exception as err:
            return handle_error(err)

    @flask_app.route('/v1/wallet/<user_id>/check/<amount>',
                     methods=['GET'])
    def check_wallet_for_amount(user_id, amount) -> Response:
        try:
            amount = Decimal(amount).quantize(Decimal('1.00'))
            data = query_service.check_available_amount(user_id, amount)
            return json.dumps(data)
        except Exception as err:
            return handle_error(err)

    @flask_app.route('/v1/wallet/<user_id>/transactions',
                     methods=['GET'])
    def get_wallet_recent_transactions(user_id) -> Response:
        try:
            token = request.headers.get('Authorization')
            security.validate_owner(token, user_id)

            data = query_service.get_wallet_recent_transactions(user_id)
            return json.dumps(data)
        except Exception as err:
            return handle_error(err)

    @flask_app.route('/v1/wallet/<user_id>/alltransactions',
                     methods=['GET'])
    def get_wallet_all_transactions(user_id) -> Response:
        try:
            token = request.headers.get('Authorization')
            security.validate_owner(token, user_id)

            data = query_service.get_wallet_all_transactions(user_id)
            return json.dumps(data)
        except Exception as err:
            return handle_error(err)

    @flask_app.route('/v1/wallet/transaction/<transaction_id>',
                     methods=['GET'])
    def check_transaction_status(transaction_id) -> Response:
        try:
            token = request.headers.get('Authorization')

            data = query_service.get_transaction(transaction_id)

            sec_data = {
                '_id_orig': data.wallet_src,
                '_id_dest': data.wallet_dst,
            }
            security.validate_party(token, sec_data)

            return json.dumps(data)
        except Exception as err:
            return handle_error(err)

    # Commands
    @flask_app.route('/v1/wallet/<user_id>/active',
                     methods=['POST'])
    def modify_wallet_status(user_id) -> Response:
        try:
            token = request.headers.get('Authorization')
            security.validate_owner_or_admin_role(token)

            params = json.loads(request.data)
            data = command_service.update_status(user_id, params)
            return json.dumps(data)
        except Exception as err:
            return handle_error(err)

    @flask_app.route('/v1/wallet/transaction',
                     methods=['POST'])
    def create_transaction() -> Response:
        try:
            token = request.headers.get('Authorization')
            params = json.loads(request.data)
            security.validate_party(token, params)

            data = command_service.create_transaction(params)
            return json.dumps(data)
        except Exception as err:
            return handle_error(err)
