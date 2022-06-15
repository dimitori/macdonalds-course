import logging

from aiogram import Bot, Dispatcher, executor, types
import httpx
from aiogram.dispatcher.filters import Text

bot = Bot(token="5576202051:AAEi0bNoA8-JHrB30eG1sQfV_TnNn1bvBSc")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


async def get_cashiers() -> list[str]:
    async with httpx.AsyncClient() as client:
        res = await client.get('http://127.0.0.1:9000/show_cashiers')
        return res.json()


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["show", "choose", "make_order"]
    keyboard.add(*buttons)
    await message.answer("Команды: ", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "show")
async def cmd_show(message: types.Message):
    cashiers = await get_cashiers()
    await message.reply("\n".join(cashiers))


@dp.message_handler(lambda message: message.text == "choose")
async def cmd_choose(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cashiers = await get_cashiers()

    keys = [
        types.InlineKeyboardButton(text=cashier, callback_data=f"choose_c_{i+1}")
        for i, cashier in enumerate(cashiers)
    ]

    keyboard.add(*keys)
    await message.answer("Какого кассира выберете?", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "make_order")
async def cmd_make_order(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cashiers = await get_cashiers()

    keys = [
        types.InlineKeyboardButton(text=cashier, callback_data=f"make_order_with_c_{i+1}")
        for i, cashier in enumerate(cashiers)
    ]

    keyboard.add(*keys)
    await message.answer("Какой кассир освободился?", reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith="choose_c_"))
async def callbacks_choose(call: types.CallbackQuery):
    index = call.data.split("_")[-1]

    async with httpx.AsyncClient() as client:
        res = await client.post(f'http://127.0.0.1:9000/choose_cashier?id_={index}')
        json_res = res.json()
        cashiers = await get_cashiers()
        await call.message.edit_text("\n".join(cashiers))

    await call.message.answer(json_res)
    await call.answer()


@dp.callback_query_handler(Text(startswith="make_order_with_c_"))
async def callbacks_make_order(call: types.CallbackQuery):
    cashier_id = call.data.split("_")[-1]

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f'http://127.0.0.1:9000/make_order',
            json={"id": cashier_id},
        )
        json_res = res.json()
        cashiers = await get_cashiers()
        await call.message.edit_text("\n".join(cashiers))

    await call.message.answer(json_res)
    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
