import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='market_making.db'):
        self.db_name = db_name
        if not self.database_exists():
            raise FileNotFoundError(f"Database '{db_name}' does not exist.")
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def database_exists(self):
        return os.path.exists(self.db_name)

    def create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            price REAL,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Balances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eth_balance REAL,
            usd_balance REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def add_transaction(self, type, price, amount):
        self.cursor.execute('''
        INSERT INTO Transactions (type, price, amount)
        VALUES (?, ?, ?)
        ''', (type, price, amount))
        self.conn.commit()
        print(f"Added transaction: {type} {price} {amount}")

    def update_balance(self, eth_balance, usd_balance):
        self.cursor.execute('''
        INSERT INTO Balances (eth_balance, usd_balance)
        VALUES (?, ?)
        ''', (eth_balance, usd_balance))
        self.conn.commit()
        print(f"Updated balance: {eth_balance} {usd_balance}")

    def get_recent_transactions(self, limit=10):
        self.cursor.execute('''
        SELECT * FROM Transactions
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def get_latest_balance(self):
        self.cursor.execute('''
        SELECT * FROM Balances
        ORDER BY timestamp DESC
        LIMIT 1
        ''')
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    db = Database()
    print(db.get_recent_transactions())
    print(db.get_latest_balance())
