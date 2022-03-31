import asyncio
from queue import Queue
import random
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Product:
    name: str
    price: float

    def prepare(self):
        pass

    def __repr__(self):  # магический метод (дандер метод)
        return f'{self.name}={self.price}'


@dataclass(repr=False)
class CookableProduct(Product):
    def prepare(self):
        self.cook()
        self.put_on_desk()

    def cook(self):
        pass


@dataclass(repr=False)
class AssemblingProduct(Product):
    def prepare(self):
        self.assemble()

    def assemble(self):
        pass


@dataclass
class Cashier:
    id: int
    balance: float
    is_free: bool = True

    async def do_work(self):
        wait_sec = random.randint(2, 20)
        print(f"кассир {self.id} будет готов через {wait_sec} секунд")
        await asyncio.sleep(wait_sec)
        self.is_free = True
        print(f"now cashier{self.id} is free")

    def _change_balance(self, money: float) -> None:
        self.balance += money

    def _get_balance(self) -> float:
        print(f'Balance cashier {self.id} now is {self.balance}')
        return self.balance

    def get_order(self, cost: float, products: list[Product]):
        print(f'Order accepted: {products}, cost={cost}')
        self._change_balance(cost)
        self._get_balance()
        self._register_order()

    def give_order(self):
        pass

    def _register_order(self) -> 'Order':
        pass


@dataclass
class Order:
    cost: float
    products: list[Product] = field(default_factory=list)
    is_ready: bool = False
    id: int = field(init=False)

    _id: ClassVar[int] = 0

    queue_orders: ClassVar[Queue] = Queue()

    def __post_init__(self):
        Order._id += 1
        self.id = Order._id
        Order.queue_orders.put(self)
        print(f'Order #{self.id} is processed:product {self.products} and cost={self.cost}')

    @staticmethod
    def get_order():
        return Order.queue_orders.get()


@dataclass
class Chef:
    id: int
    cooking_time: float = 0
    is_free: bool = True

    async def cook(self, order: Order):
        print(f'Chef {self.id} start cooking order #{order.id} time of prepare:{self.calculate_time(order)}')
        self.is_free = False
        await asyncio.sleep(self.calculate_time(order))
        order.is_ready = True
        self.is_free = True
        print(f'Chef cooked order #{order.id}')

    @staticmethod
    def calculate_time(order: Order) -> int:
        return sum([2 if i is CookableProduct else 1 for i in order.products])


@dataclass
class Client:
    id: int
    money: float
    chosen_products: list = field(default_factory=list)

    def form_order(self, cost: float) -> Order:
        return Order(cost, self.chosen_products)

    @staticmethod
    async def _choose_cashier(cashiers: list[Cashier]) -> Cashier:
        free_cashier = None

        while not free_cashier:

            for cashier in cashiers:
                if cashier.is_free:
                    free_cashier = cashier

            if not free_cashier:
                wait_sec = 2
                print(f"Никто не нашелся, ждем {wait_sec} сек")
                await asyncio.sleep(wait_sec)

        print(f"{free_cashier} chosen")
        return free_cashier

    @staticmethod
    async def chose_chefs(chefs: list[Chef]):
        free_chef = None

        while not free_chef:

            for chef in chefs:
                if chef.is_free:
                    free_chef = chef

            if not free_chef:
                wait_sec = 2
                print(f"Шефы заняты, ждем {wait_sec} сек")
                await asyncio.sleep(wait_sec)

        print(f"{free_chef} chosen")
        return free_chef

    async def buy(self, products: list[Product], cashiers: list[Cashier], chefs: list[Chef]):
        self._choose_products(products)
        cost = self._prepare_money()
        print(f'Client{self.id} chose {self.chosen_products} with cost={cost}')

        cashier = await self._choose_cashier(cashiers)

        if self.chosen_products:
            self._pay(cost, cashier)

        order = self.form_order(cost)
        chef = await self.chose_chefs(chefs)
        await chef.cook(order.get_order())

    def _pay(self, cost: float, cashier: Cashier) -> None:
        self.money -= cost
        cashier.get_order(cost, self.chosen_products)

    def _prepare_money(self) -> float:
        while self.chosen_products:
            cost = sum([p.price for p in self.chosen_products])
            if cost < self.money:
                return cost
            self._reduce_products()
        return 0.0

    def _choose_products(self, products: list[Product]) -> None:
        if not self.chosen_products:
            count = random.randint(1, 10)
            self.chosen_products = [random.choice(products) for _ in range(count)]  # генераторное выражение
        else:
            print('choose nothing, have alredy')

    def _reduce_products(self) -> None:
        self.chosen_products.pop()


async def main():
    product1 = CookableProduct('burger', price=3.00)
    product2 = CookableProduct('fries', 2.00)
    product3 = AssemblingProduct('Coffee', 1.00)

    products = [product1, product2, product3]

    client = Client(1, 10)
    client1 = Client(2, 14)
    client2 = Client(3, 10)
    clients = [client, client1, client2]
    chef = Chef(1)
    chef2 = Chef(2)
    chefs = [chef, chef2]
    cashier1 = Cashier(1, balance=random.randint(0, 10), is_free=random.randint(0, 1))
    cashier2 = Cashier(2, balance=random.randint(0, 10), is_free=random.randint(0, 1))
    cashier3 = Cashier(3, balance=random.randint(0, 10), is_free=random.randint(0, 1))
    cashiers = [cashier1, cashier2, cashier3]

    async def counter():
        count = 0
        for _ in range(30):
            print(f'time: {count}')
            await asyncio.sleep(1)
            count += 1

    await asyncio.gather(
        counter(),
        *[client.buy(products, cashiers, chefs) for client in clients],
        *[c.do_work() for c in cashiers],

    )


asyncio.run(main())
