import logging

from aiogram import Bot, Dispatcher, executor, types
import httpx

bot = Bot(token="5576202051:AAEi0bNoA8-JHrB30eG1sQfV_TnNn1bvBSc")
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


@dp.message_handler(commands="show")
async def cmd_show(message: types.Message):
    async with httpx.AsyncClient() as client:
        res = await client.get('http://127.0.0.1:9000/show_cashiers')
        res_json: list[str] = res.json()
    await message.reply("\n".join(res_json))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
