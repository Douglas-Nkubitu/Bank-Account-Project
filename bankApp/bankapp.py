from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize account details
account = {
    "account_balance": 0,
    "total_deposits_today": 0,
    "total_withdrawals_today": 0,
    "deposit_transactions_today": 0,
    "withdrawal_transactions_today": 0
}

# Constants for constraints
MAX_DEPOSIT_PER_TRANSACTION = 40000
MAX_DEPOSIT_FREQUENCY_PER_DAY = 4
MAX_DEPOSIT_PER_DAY = 150000
MAX_WITHDRAWAL_PER_TRANSACTION = 20000
MAX_WITHDRAWAL_FREQUENCY_PER_DAY = 3
MAX_WITHDRAWAL_PER_DAY = 50000

@app.route("/home")
def index():
    return render_template('home.html')

@app.route('/balance', methods=['GET'])
def get_balance():
    return jsonify({'balance': account["account_balance"]})

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

if __name__ == '__main__':
    app.run()