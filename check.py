from flask import Flask
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

with app.app_context():
    transactions = Transaction.query.all()

    if transactions:
        for t in transactions:
            print(f"ID: {t.id}, Account: {t.account}, Type: {t.type}, Amount: {t.amount}, Description: {t.description}, Date: {t.date}")
    else:
        print("Таблица Transaction пуста.")
