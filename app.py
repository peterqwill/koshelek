from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)

# Добавляем 4 счета
accounts = {
    'account_1': 'Нал',
    'account_2': 'Перевод',
    'account_3': 'Счёт',
    'account_4': 'Макс'
}

# Подсчёт баланса по каждому счёту
def calculate_balances():
    balances = {key: 0 for key in accounts.keys()}
    transactions = Transaction.query.all()
    for transaction in transactions:
        if transaction.type == 'income':
            balances[transaction.account] += transaction.amount
        elif transaction.type == 'expense':
            balances[transaction.account] -= transaction.amount
    return balances

@app.route('/')
def index():
    transactions = Transaction.query.all()
    balances = calculate_balances()
    return render_template('index.html', transactions=transactions, accounts=accounts, balances=balances)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    account = request.form['account']
    type = request.form['type']
    amount = float(request.form['amount'])
    description = request.form['description']
    date = request.form['date']

    new_transaction = Transaction(account=account, type=type, amount=amount, description=description, date=date)
    db.session.add(new_transaction)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get(transaction_id)
    if transaction:
        db.session.delete(transaction)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
