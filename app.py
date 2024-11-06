import re
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Регулярное выражение для поиска "ЗП" в любом регистре
pattern = re.compile(r'\bзп\b', re.IGNORECASE)

# Подсчёт балансов (все транзакции учитываются, включая расходы с "ЗП")
def calculate_balances():
    balances = {key: 0 for key in accounts.keys()}
    transactions = Transaction.query.all()  # Получаем все транзакции
    for transaction in transactions:
        if transaction.type == 'income':
            balances[transaction.account] += transaction.amount
        elif transaction.type == 'expense':
            # Все расходы учитываются, включая с "ЗП", для расчета балансов
            balances[transaction.account] -= transaction.amount
    return balances

# Подсчёт общего дохода (все доходы учитываются)
def calculate_total_income():
    total_income = 0
    transactions = Transaction.query.filter_by(type='income').all()
    for transaction in transactions:
        total_income += transaction.amount
    return total_income

# Подсчёт общего расхода (фильтруем расходы с "ЗП" из расчета)
def calculate_total_expense():
    total_expense = 0
    transactions = Transaction.query.filter_by(type='expense').all()
    for transaction in transactions:
        # Исключаем расходы с "ЗП" из общего расчета
        if not pattern.search(transaction.description):  
            total_expense += transaction.amount
    return total_expense

# Модель для транзакций
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)

# Модель для ожидаемых приходов
class ExpectedIncome(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)

# Счета
accounts = {
    'account_1': 'Нал',
    'account_2': 'Перевод',
    'account_3': 'Счёт',
    'account_4': 'Макс'
}

# Главная страница
@app.route('/')
def index():
    transactions = Transaction.query.all()  # Получаем все транзакции
    balances = calculate_balances()  # Подсчитаем балансы (включая расходы с "ЗП")
    expected_incomes = ExpectedIncome.query.all()
    total_income = calculate_total_income()  # Подсчитаем общий доход
    total_expense = calculate_total_expense()  # Подсчитаем общий расход (без "ЗП")
    
    return render_template(
        'index.html',
        transactions=transactions,  # Отображаем все транзакции
        accounts=accounts,
        balances=balances,
        expected_incomes=expected_incomes,
        total_income=total_income,
        total_expense=total_expense
    )

# Добавить транзакцию
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    account = request.form['account']
    trans_type = request.form['type']
    amount = float(request.form['amount'])
    description = request.form['description']
    date = request.form['date']
    new_transaction = Transaction(account=account, type=trans_type, amount=amount, description=description, date=date)
    db.session.add(new_transaction)
    db.session.commit()
    return redirect(url_for('index'))

# Добавить ожидаемый приход
@app.route('/add_expected_income', methods=['POST'])
def add_expected_income():
    account = request.form['account']
    amount = float(request.form['amount'])
    description = request.form['description']
    date = request.form['date']
    new_income = ExpectedIncome(account=account, amount=amount, description=description, date=date)
    db.session.add(new_income)
    db.session.commit()
    return redirect(url_for('index'))

# Удалить ожидаемый приход
@app.route('/delete_expected_income/<int:id>', methods=['POST'])
def delete_expected_income(id):
    income = ExpectedIncome.query.get_or_404(id)
    db.session.delete(income)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
