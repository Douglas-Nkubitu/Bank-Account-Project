from flask import Flask, render_template, request, jsonify
from itertools import count

app = Flask(__name__)

# Initialize account details
account = {
    "account_balance": 0,
    "total_deposits_today": 0,
    "total_withdrawals_today": 0,
    "deposit_transactions_today": 0,
    "withdrawal_transactions_today": 0,
    "account_id": None,
    "customer_id": None
}

# Constants for constraints
MAX_DEPOSIT_PER_TRANSACTION = 40000
MAX_DEPOSIT_FREQUENCY_PER_DAY = 4
MAX_DEPOSIT_PER_DAY = 150000
MAX_WITHDRAWAL_PER_TRANSACTION = 20000
MAX_WITHDRAWAL_FREQUENCY_PER_DAY = 3
MAX_WITHDRAWAL_PER_DAY = 50000

#Incremental Account and Customer IDs
account_id_counter = count(start=0)
customer_id_counter = count(start=0)

@app.route("/")
def index():
    return render_template('home.html')

# Get Balance
@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({'balance': account["account_balance"]})

# Deposit
@app.route('/deposit', methods=['POST'])
def deposit():
    amount = request.json.get('amount', 0)
    
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    
    amount = float(amount)
    
    if amount > MAX_DEPOSIT_PER_TRANSACTION:
        return jsonify({'error': 'Exceeded Maximum Deposit Per Transaction'}), 400
    
    if account["total_deposits_today"] + amount > MAX_DEPOSIT_PER_DAY:
        return jsonify({'error': 'Exceeded Maximum Deposit Per Day'}), 400
    
    if account["deposit_transactions_today"] >= MAX_DEPOSIT_FREQUENCY_PER_DAY:
        return jsonify({'error': 'Exceeded Maximum Deposit Frequency Per Day'}), 400
    
    # Update account details
    account["account_balance"] += amount
    account["total_deposits_today"] += amount
    account["deposit_transactions_today"] += 1
    
    return jsonify({'message': 'Deposit successful'})

# Withdrawal
@app.route('/withdrawal', methods=['POST'])
def withdrawal():
    amount = request.json.get('amount', 0)
    
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
    
    amount = float(amount)
    
    if amount > account["account_balance"]:
        return jsonify({'error': 'Insufficient balance'}), 400
    
    if amount > MAX_WITHDRAWAL_PER_TRANSACTION:
        return jsonify({'error': 'Exceeded Maximum Withdrawal Per Transaction'}), 400
    
    if account["total_withdrawals_today"] + amount > MAX_WITHDRAWAL_PER_DAY:
        return jsonify({'error': 'Exceeded Maximum Withdrawal Per Day'}), 400
    
    if account["withdrawal_transactions_today"] >= MAX_WITHDRAWAL_FREQUENCY_PER_DAY:
        return jsonify({'error': 'Exceeded Maximum Withdrawal Frequency Per Day'}), 400
    
    # Update account details
    account["account_balance"] -= amount
    account["total_withdrawals_today"] += amount
    account["withdrawal_transactions_today"] += 1
    
    return jsonify({'message': 'Withdrawal successful'})

# Create Account
@app.route('/create_account', methods=['POST'])
def create_account():
    # Generate incremental IDs
    account_id = next(account_id_counter)
    customer_id = next(customer_id_counter)
    
    # Store IDs in the account object
    account['account_id'] = account_id
    account['customer_id'] = customer_id
    
    return jsonify({'message': 'Account created successfully', 'account_id': account_id, 'customer_id': customer_id})

if __name__ == '__main__':
    app.run(debug=True)