import asyncio
import copy
import random
from dataclasses import dataclass
from orders_queue import orders_queue
from orders import Order
from objects import products


class CashierNotFree(Exception):
    pass


@dataclass
class Cashier:
    id: int
    balance: float
    orders_queue: list[Order]
    is_free: bool = True

    async def do_work(self):
        wait_sec = random.randint(10, 20)
        print(f"кассир {self.id} будет готов через {wait_sec} секунд")
        await asyncio.sleep(wait_sec)
        self.is_free = True
        print(f"now cashier{self.id} is free")

    def _change_balance(self, money: float) -> None:
        self.balance += money

    def _get_balance(self) -> float:
        print(f'Balance cashier {self.id} now is {self.balance}')
        return self.balance

    def get_order(self, order: Order):
        print(f'Order accepted: {order}')
        self._change_balance(order.cost)
        self._get_balance()
        self._register_order(order)

    def give_order(self):
        pass

    def _register_order(self, order) -> None:
        self.orders_queue.append(order)


cashier1 = Cashier(1, balance=random.randint(0, 10), is_free=random.choice([True, False]), orders_queue=orders_queue)
cashier2 = Cashier(2, balance=random.randint(0, 10), is_free=random.choice([True, False]), orders_queue=orders_queue)
cashier3 = Cashier(3, balance=random.randint(0, 10), is_free=random.choice([True, False]), orders_queue=orders_queue)


cashiers = [cashier1, cashier2, cashier3]

def show_products():
    return [f"продукт - {p.name}" for p in products]

def show_cashiers():
    return [f"кассир{c.id} = {c.is_free}" for c in cashiers]


def choose_cashier(id_: int) -> Cashier:
    cashier = cashiers[id_-1]
    if cashier.is_free:
        cashier.is_free = False
        return cashier
    raise CashierNotFree()


def make_order(id_: int, products: list, cost:float):
    new_products = copy.deepcopy(products)
    cashier = cashiers[id_-1]
    cashier.is_free = True
    order = Order(cost, new_products)
    return order



