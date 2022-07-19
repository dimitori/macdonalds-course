import asyncio
import sys
import copy

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
sys.path.append('/Users/nikitaklinchev/PycharmProjects/boot_telegram/macdonalds-course')
from cashiers import cashiers, show_cashiers, choose_cashier, CashierNotFree, make_order, show_products, products
from chefs import chefs
from objects import choosen_products, _calculate_money
from orders_queue import orders_queue

app = FastAPI()


class Cashier(BaseModel):
    id: int


class CashierNotFreeNow(Exception):
    status_code = 500
    message = "Cashier not free now"
    code = "cashier_not_free"


async def run_staff_routine():
    await asyncio.gather(
        *[c.do_work() for c in cashiers],
        *[c.do_work() for c in chefs],
    )


@app.on_event('startup')
async def app_startup():
    asyncio.create_task(run_staff_routine())


@app.get("/show_cashiers")
async def show_cashiers_() -> list[str]:
    return show_cashiers()

@app.get("/show_products")
async def show_products_() -> list[str]:
    return show_products()


@app.post("/choose_cashier")
async def choose_cashier_(id_: int):
    try:
        cashier = choose_cashier(id_)
        return f"Кассир {cashier.id} выбран"
    except CashierNotFree:
        raise HTTPException(status_code=409, detail="Кассир уже занят")


@app.post("/make_order")
async def make_order_(cashier: Cashier):
    cost = _calculate_money(choosen_products)
    orders_queue.append(make_order(cashier.id, choosen_products, cost))
    choosen_products.clear()
    Products = []
    for i in range(len(orders_queue[-1].products)):
       Products.append((orders_queue[-1].products[i].name))

    return f"Кассир {cashier.id} освободился, " \
           f"продукты  {','.join(Products)} в заказе, стоимость заказа {cost}"

@app.post('/choose_cashier')
async def choose_cashier_(id_:int):
    cashier = choose_cashier(id_)
    return f"Кассир {cashier.id} выбраннн"

@app.get('/show_cashiers')
async def show_all_cashiers():
    return show_cashiers()

# @app.get('/show_chefs')
# async def show_all_chefs():
#     return show_chefs()
#
# @app.post('/choose_chefs')
# async def choose_chefs_(id_:int):
#     chef = choose_chefs(id_)
#     return f"Повар {chef.id} выбран, время приготовления {chef.cooking_time} cекунд"
#
# @app.post('/choose_chefs')
# async def choose_chefs_(id_:int):
#     chef = choose_chefs(id_)
#     return f"Повар {chef.id} выбран, время приготовления {chef.cooking_time} cекунд"

@app.get('/show_chosen_products')
async def show_chosen_products():
    return [f"продукт {c.name} выбран" for c in choosen_products]

@app.post('/choose_products')
async def choose_products_(number:int):
    product = products[number-1]
    choosen_products.append(product)
    return f"Продукт  {product.name} выбран"

@app.get('/show_orders')
async def show_orders():
    return [f"Заказ №{order.id} {order.is_ready} " \
            f"с продуктами {order.products}" for order in orders_queue]

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
