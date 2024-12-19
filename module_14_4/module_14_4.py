import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.storage.memory import MemoryStorage

import constances
from main_menu_router import main_menu_router
from calories_count_router import calories_count_router
from product_router import product_buy_router


bot = Bot(token=constances.api)
dp = Dispatcher(storage=MemoryStorage())

default_router = Router()

@default_router.message()
async def any_other_message(message: types.Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение.")

async def main():
    dp.include_routers(main_menu_router, calories_count_router, product_buy_router, default_router)
    await bot.delete_webhook(drop_pending_updates=True) #  Используется для игнорирования все накопленных входящих
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())