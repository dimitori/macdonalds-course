import asyncio
from dataclasses import dataclass

from orders import Order
from products import CookableProduct


@dataclass
class Chef:
    id: int
    orders_queue: list[Order]
    cooking_time: float = 0
    is_free: bool = True

    async def do_work(self):
        while True:
            await asyncio.sleep(3)
            if self.orders_queue:
                order = self.orders_queue.pop()
                print(f"повар {self.id} забрал заказ {order}")
                await self.cook(order)

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