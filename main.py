import asyncio

import random
from dataclasses import dataclass, field


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
class Chef:
    id: int
    is_free: int

    def cook(self):
        pass


@dataclass
class Order:
    id: int


@dataclass
class Client:
    id: int
    money: float
    chosen_products: list = field(default_factory=list)

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

    async def buy(self, products: list[Product], cashiers: list[Cashier]):
        self._choose_products(products)
        cost = self._prepare_money()
        print(f'Client{self.id} chose {self.chosen_products} with cost={cost}')

        cashier = await self._choose_cashier(cashiers)

        if self.chosen_products:
            self._pay(cost, cashier)

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
        count = random.randint(1, 10)
        self.chosen_products = [random.choice(products) for _ in range(count)]  # генераторное выражение

    def _reduce_products(self) -> None:
        self.chosen_products.pop()


async def main():
    product1 = CookableProduct('burger', price=3.00)
    product2 = CookableProduct('fries', 2.00)
    product3 = AssemblingProduct('Coffee', 1.00)

    products = [product1, product2, product3]

    client = Client(1, 10)
    cashier1 = Cashier(1, balance=random.randint(0, 10), is_free=False)
    cashier2 = Cashier(2, balance=random.randint(0, 10), is_free=False)
    cashier3 = Cashier(3, balance=random.randint(0, 10), is_free=False)
    cashiers = [cashier1, cashier2, cashier3]

    await asyncio.gather(
        client.buy(products, cashiers),
        *[c.do_work() for c in cashiers],
    )

asyncio.run(main())
