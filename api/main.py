import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException

from cashiers import cashiers, show_cashiers, choose_cashier, CashierNotFree, make_order
from objects import chefs

app = FastAPI()


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


@app.post("/choose_cashier")
async def choose_cashier_(id_: int):
    try:
        cashier = choose_cashier(id_)
        return f"Кассир {cashier.id} выбран"
    except CashierNotFree:
        raise HTTPException(status_code=409, detail="Кассир уже занят")


@app.post("/make_order")
async def make_order_(id_: int):
    make_order(id_)
    return f"Кассир {id_} освободился"


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
