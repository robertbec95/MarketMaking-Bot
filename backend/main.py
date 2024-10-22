import requests
import time
import random
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class Order:
    side: str
    price: float
    amount: float

class MarketMaker:
    def __init__(self, eth_balance: float, usd_balance: float):
        self.eth_balance = eth_balance
        self.usd_balance = usd_balance
        self.orders: List[Order] = []
        self.last_balance_print = time.time() 

    def get_order_book(self) -> Dict:
        url = "https://api.deversifi.com/bfx/v2/book/tETHUSD/R0"
        response = requests.get(url)
        return response.json()

    def place_orders(self, best_bid: float, best_ask: float):
        for _ in range(5):
            bid_price = round(random.uniform(best_bid * 0.95, best_bid), 2)
            ask_price = round(random.uniform(best_ask, best_ask * 1.05), 2)
            bid_amount = round(random.uniform(0.1, 1.0), 4)
            ask_amount = round(random.uniform(0.1, 1.0), 4)

            if self.usd_balance >= bid_price * bid_amount:
                self.orders.append(Order("BID", bid_price, bid_amount))
                print(f"PLACE BID @ {bid_price} {bid_amount}")

            if self.eth_balance >= ask_amount:
                self.orders.append(Order("ASK", ask_price, ask_amount))
                print(f"PLACE ASK @ {ask_price} {ask_amount}")

    def check_filled_orders(self, best_bid: float, best_ask: float):
        filled_orders = []
        for order in self.orders:
            if (order.side == "BID" and order.price > best_bid) or \
               (order.side == "ASK" and order.price < best_ask):
                filled_orders.append(order)

        for order in filled_orders:
            self.orders.remove(order)
            if order.side == "BID":
                self.eth_balance += order.amount
                self.usd_balance -= order.price * order.amount
                print(f"FILLED BID @ {order.price} {order.amount} (ETH + {order.amount} USD - {order.price * order.amount})")
            else:
                self.eth_balance -= order.amount
                self.usd_balance += order.price * order.amount
                print(f"FILLED ASK @ {order.price} {order.amount} (ETH - {order.amount} USD + {order.price * order.amount})")

    def print_balances(self):
        print(f"ETH Balance: {self.eth_balance:.4f}")
        print(f"USD Balance: {self.usd_balance:.2f}")

    def run(self):
        while True:
            order_book = self.get_order_book()
            best_bid = order_book[0][1]
            best_ask = order_book[-1][1]

            self.check_filled_orders(best_bid, best_ask)
            self.place_orders(best_bid, best_ask)

            if time.time() - self.last_balance_print >= 30:
                self.print_balances()
                self.last_balance_print = time.time()

            time.sleep(5)

if __name__ == "__main__":
    bot = MarketMaker(10, 2000)
    bot.run()