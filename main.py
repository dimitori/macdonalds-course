import asyncio
import random
from dataclasses import dataclass, field
from cashiers import Cashier
from chefs import Chef
from orders import Order
from products import Product


@dataclass
class Client:
    id: int
    money: float
    chosen_products: list = field(default_factory=list)

    def form_order(self, cost: float) -> Order:
        return Order(cost, self.chosen_products)

    @staticmethod
    async def _choose_cashier(cashiers: list['Cashier']) -> 'Cashier':
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

    async def buy(self, products: list[Product], cashiers: list[Cashier]):
        self._choose_products(products)
        cost = self._prepare_money()
        print(f'Client{self.id} chose {self.chosen_products} with cost={cost}')

        cashier = await self._choose_cashier(cashiers)

        if self.chosen_products:
            order = self.form_order(cost)
            self._pay(order, cashier)

    def _pay(self, order: Order, cashier: Cashier) -> None:
        self.money -= order.cost
        cashier.get_order(order)

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
    from objects import chefs
    from cashiers import cashiers

    async def counter():
        count = 0
        while True:
            print(f'time: {count}')
            await asyncio.sleep(1)
            count += 1

    await asyncio.gather(
        counter(),
        *[c.do_work() for c in cashiers],
        *[c.do_work() for c in chefs],
    )


if __name__ == "__main__":
    asyncio.run(main())
