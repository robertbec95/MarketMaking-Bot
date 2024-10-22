import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='market_making.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            price REAL,
            amount REAL,
            timestamp DATETIME
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eth_balance REAL,
            usd_balance REAL,
            timestamp DATETIME
        )
        ''')
        self.conn.commit()

    def add_transaction(self, type, price, amount):
        self.cursor.execute('''
        INSERT INTO transactions (type, price, amount, timestamp)
        VALUES (?, ?, ?, ?)
        ''', (type, price, amount, datetime.now()))
        self.conn.commit()
        print(f"Added transaction: {type} {price} {amount} {datetime.now()}")

    def update_balance(self, eth_balance, usd_balance):
        self.cursor.execute('''
        INSERT INTO balances (eth_balance, usd_balance, timestamp)
        VALUES (?, ?, ?)
        ''', (eth_balance, usd_balance, datetime.now()))
        self.conn.commit()
        print(f"Updated balance: {eth_balance} {usd_balance} {datetime.now()}")
    def get_recent_transactions(self, limit=10):
        self.cursor.execute('''
        SELECT * FROM transactions
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def get_latest_balance(self):
        self.cursor.execute('''
        SELECT * FROM balances
        ORDER BY timestamp DESC
        LIMIT 1
        ''')
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()