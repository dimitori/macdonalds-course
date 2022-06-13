import random

from orders_queue import orders_queue
from products import CookableProduct, AssemblingProduct
from chefs import Chef
from cashiers import Cashier

product1 = CookableProduct('burger', price=3.00)
product2 = CookableProduct('fries', 2.00)
product3 = AssemblingProduct('Coffee', 1.00)


chef = Chef(1, orders_queue)
chef2 = Chef(2, orders_queue)

cashier = Cashier(1, balance=random.randint(0, 10), is_free=True, orders_queue=orders_queue)


products = [product1, product2, product3]
chefs = [chef, chef2]
