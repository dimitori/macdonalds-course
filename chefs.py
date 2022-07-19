import asyncio
import random
from dataclasses import dataclass
from orders import Order
from products import CookableProduct
from orders_queue import orders_queue

class ChefsNotFree(Exception):
    pass

@dataclass
class Chef:
    id: int
    orders_queue: list[Order]
    cooking_time: float = 4
    is_free: bool = True

    async def do_work(self):
        while True:
            await asyncio.sleep(5)
            for order in orders_queue:
                if order.is_ready == False:
                    print(f"повар {self.id} забрал заказ {order}")
                    self.cooking_time = self.calculate_time(order)
                    await self.cook(order)


    async def cook(self, order: Order):
        print(f'Chef {self.id} start cooking order #{order.id} time of prepare:{self.calculate_time(order)}')
        self.is_free = False
        order.is_ready = True
        await asyncio.sleep(self.calculate_time(order))
        self.is_free = True
        print(f'Chef cooked order #{order.id}')

    @staticmethod
    def calculate_time(order: Order) -> int:
        return sum([2 if i is CookableProduct else 1 for i in order.products])


chef = Chef(1, orders_queue)
chef2 = Chef(2, orders_queue)
chef3 = Chef(3, orders_queue)
chefs = [chef, chef2, chef3]

# def show_chefs():
#     c =[f"повар{c.id} = {c.is_free} освободится через {c.cooking_time} секунд" for c in chefs]
#     print(c)
#     return c
#
# def choose_chefs(id:int) -> Chef:
#     chef = chefs[id-1]
#     if chef.is_free == True:
#         chef.is_free = False
#         return chef
#     raise ChefsNotFree()