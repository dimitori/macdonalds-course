import random

from orders_queue import orders_queue
from products import CookableProduct, AssemblingProduct

product  = CookableProduct('burger', price=3.00)
product2 = CookableProduct('fries', 2.00)
product3 = AssemblingProduct('Coffee', 1.00)

products = [product, product2, product3]

choosen_products = []

def _calculate_money(chosen_products) -> float:
    while chosen_products:
        cost = sum([p.price for p in chosen_products])
        return cost
