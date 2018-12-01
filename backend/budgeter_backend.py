from flask import Flask, request
from flask_restful import Resource, Api

import random
import string

import backend.budgeter_db as db

app = Flask(__name__)
api = Api(app)

auth_users = ['daria', 'venio', 'someone_other']


class Accounts(Resource):
    def get(self, uid):
        user_accounts = db.db_get_accounts(uid)
        return {
            'accounts': user_accounts
        }

    def put(self, uid):
        if 'account_name' not in request.json or 'init_balance' not in request.json:
            return {'status': 'FAIL', 'message': 'Malformed request'}
        account_name = request.json['account_name']
        init_balance = request.json['init_balance']
        account_id = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16))
        return db.db_add_account(account_id, account_name, uid, init_balance)

    def delete(self, uid, account_id):
        return db.db_delete_account(uid, account_id)

    def patch(self, uid, account_id):
        if 'new_balance' not in request.json:
            return {'status': 'FAIL', 'message': 'Malformed request'}
        new_balance = request.json['new_balance']
        return db.db_modify_account_balance(uid, account_id, new_balance)


class Transactions(Resource):
    def get(self, uid):
        accounts = [account['_id'] for account in db.db_get_accounts(uid)]
        transactions = db.db_get_transactions(accounts)
        return {
            'transactions': transactions
        }

    def put(self, uid):
        if ('account_from' not in request.json or 'account_to' not in request.json
                or 'amount' not in request.json or 'currency' not in request.json or 'timestamp' not in request.json):
            return {'status': 'FAIL', 'message': 'Malformed request'}
        account_from = request.json['account_from']
        accont_to = request.json['account_to']
        amount = request.json['amount']
        currency = request.json['currency']
        timestamp = request.json['timestamp']
        transaction_id = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(32))
        return db.db_add_transaction(transaction_id, account_from, accont_to, amount, currency, timestamp)


api.add_resource(Accounts, '/accounts/<string:uid>', '/accounts/<string:uid>/<string:account_id>')
api.add_resource(Transactions, '/transactions/<string:uid>')


if __name__ == '__main__':
    app.run(port='10000', debug=True)
