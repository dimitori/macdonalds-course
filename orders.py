from asyncio import Queue
from dataclasses import dataclass, field
from typing import ClassVar

from products import Product


@dataclass
class Order:
    cost: float
    products: list[Product] = field(default_factory=list)
    is_ready: bool = False
    id: int = field(init=False)

    _id: ClassVar[int] = 0


    def __post_init__(self):
        Order._id += 1
        self.id = Order._id
        print(f'Order #{self.id} is processed:product {self.products} and cost={self.cost}')

    @staticmethod
    def get_order():
        return Order.queue_orders.get()

