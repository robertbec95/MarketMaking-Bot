import requests
import time
import random
from typing import List, Dict
from dataclasses import dataclass
from database import Database
import sys

@dataclass
class Order:
    side: str  # "BID" or "ASK"
    price: float
    amount: float

class MarketMaker:
    def __init__(self, eth_balance: float, usd_balance: float):
        self.db = None
        try:
            self.db = Database()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print("The database should be created by the frontend Prisma.")
            sys.exit(1)

        # Initialize the market maker with starting balances
        self.eth_balance = eth_balance
        self.usd_balance = usd_balance
        self.orders: List[Order] = []
        self.last_balance_print = time.time()
        self.db.update_balance(self.eth_balance, self.usd_balance) 

    def get_order_book(self) -> Dict:
        # Fetch the current order book from the exchange API
        url = "https://api.deversifi.com/bfx/v2/book/tETHUSD/R0"
        response = requests.get(url)
        return response.json()

    def place_orders(self, best_bid: float, best_ask: float):
        # Place multiple orders around the best bid and ask prices
        for _ in range(5):
            # Generate random prices and amounts for orders
            bid_price = round(random.uniform(best_bid * 0.95, best_bid), 2)
            ask_price = round(random.uniform(best_ask, best_ask * 1.05), 2)
            bid_amount = round(random.uniform(0.1, 1.0), 4)
            ask_amount = round(random.uniform(0.1, 1.0), 4)

            # Place a bid order if there's enough USD balance
            if self.usd_balance >= bid_price * bid_amount:
                self.orders.append(Order("BID", bid_price, bid_amount))
                print(f"PLACE BID @ {bid_price} {bid_amount}")
                self.db.add_transaction("PLACE_BID", bid_price, bid_amount)  

            # Place an ask order if there's enough ETH balance
            if self.eth_balance >= ask_amount:
                self.orders.append(Order("ASK", ask_price, ask_amount))
                print(f"PLACE ASK @ {ask_price} {ask_amount}")
                self.db.add_transaction("PLACE_ASK", ask_price, ask_amount)  

    def check_filled_orders(self, best_bid: float, best_ask: float):
        # Check if any existing orders have been filled
        filled_orders = []
        for order in self.orders:
            if (order.side == "BID" and order.price > best_bid) or \
               (order.side == "ASK" and order.price < best_ask):
                filled_orders.append(order)

        # Process filled orders and update balances
        for order in filled_orders:
            self.orders.remove(order)
            if order.side == "BID":
                self.eth_balance += order.amount
                self.usd_balance -= order.price * order.amount
                print(f"FILLED BID @ {order.price} {order.amount} (ETH + {order.amount} USD - {order.price * order.amount})")
                self.db.add_transaction("FILLED_BID", order.price, order.amount)  
            else:
                self.eth_balance -= order.amount
                self.usd_balance += order.price * order.amount
                print(f"FILLED ASK @ {order.price} {order.amount} (ETH - {order.amount} USD + {order.price * order.amount})")
                self.db.add_transaction("FILLED_ASK", order.price, order.amount)  
            
            self.db.update_balance(self.eth_balance, self.usd_balance)  

    def print_balances(self):
        # Print current balances and recent transactions
        print(f"ETH Balance: {self.eth_balance:.4f}")
        print(f"USD Balance: {self.usd_balance:.2f}")
        
        print("Recent transactions:")
        for transaction in self.db.get_recent_transactions(5):
            print(f"Type: {transaction[1]}, Price: {transaction[2]}, Amount: {transaction[3]}, Time: {transaction[4]}")

    def run(self):
        # Main loop for the market maker
        while True:
            # Get the current order book
            order_book = self.get_order_book()
            best_bid = order_book[0][1]
            best_ask = order_book[-1][1]

            # Check for filled orders and place new ones
            self.check_filled_orders(best_bid, best_ask)
            self.place_orders(best_bid, best_ask)

            # Print balances every 30 seconds
            if time.time() - self.last_balance_print >= 30:
                self.print_balances()
                self.last_balance_print = time.time()

            # Wait for 5 seconds before the next iteration
            time.sleep(5)

    def __del__(self):
        # Close the database connection when the object is destroyed
        if hasattr(self, 'db') and self.db is not None:
            self.db.close() 

if __name__ == "__main__":
    # Create and run the market maker with initial balances
    bot = MarketMaker(10, 2000)
    bot.run()
