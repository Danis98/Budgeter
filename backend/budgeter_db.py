import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")

db = mongo_client['budgeter_db']

# users_collection = db['users']
accounts_collection = db['accounts']
transactions_collection = db['transactions']


# add an account
def db_add_account(account_id, account_name, owner, init_balance):
    res = accounts_collection.insert_one({
        '_id': account_id,
        'account_name': account_name,
        'owner': owner,
        'balance': init_balance,
    })
    if res.acknowledged:
        return {'status': 'SUCCESS'}
    else:
        return {'status': 'FAIL', 'message': 'Could not add account to db'}


# get all accounts of a user
def db_get_accounts(owner):
    return list(accounts_collection.find({'owner': owner}))


# delete specified account
def db_delete_account(owner, account_id):
    res = accounts_collection.delete_one({
        '$and': [
            {'_id': account_id},
            {'owner': owner}
        ]
    })
    if res.acknowledged:
        return {'status': 'SUCCESS'}
    else:
        return {'status': 'FAIL', 'message': 'Could not delete account'}


# modify account balance
def db_modify_account_balance(owner, account_id, new_balance):
    res = accounts_collection.update_one({
            '$and': [
                {'owner': owner},
                {'_id': account_id}
            ]
        },
        {
            '$set': {
                'balance': new_balance
            }
        })
    if res.acknowledged:
        return {'status': 'SUCCESS'}
    else:
        return {'status': 'FAIL', 'message': 'Could not update account'}


# add transaction to db
def db_add_transaction(transaction_id, account_from, account_to, amount, currency, timestamp):
    res = transactions_collection.insert_one({
        '_id': transaction_id,
        'account_from': account_from,
        'account_to': account_to,
        'amount': amount,
        'currency': currency,
        'timestamp': timestamp,
    })
    if res.acknowledged:
        return {'status': 'SUCCESS'}
    else:
        return {'status': 'FAIL', 'message': 'Could not add transaction to db'}


# get all transactions involving the specified accounts
def db_get_transactions(accounts):
    print(accounts)
    return list(transactions_collection.find({
        '$or': [
            {'account_from': {'$in': accounts}},
            {'account_to': {'$in': accounts}}
        ]
    }))
