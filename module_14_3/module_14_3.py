from aiogram import Bot, Dispatcher,  types, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import CommandStart
from aiogram.types import  CallbackQuery, Message, InputMediaPhoto
from aiogram.types.input_file import FSInputFile
import constances
import menus as menu
import asyncio


bot = Bot(token=constances.api)
dp = Dispatcher(storage=MemoryStorage())


class UserState(StatesGroup):
    sex = State()
    age = State()
    growth = State()
    weight = State()
    product = State()
    options_answer_message: Message = None


@dp.message(CommandStart())
async def cmd_start(message: types.Message, state) -> None:
    UserState.options_answer_message = message
    await state.set_state(UserState.sex)
    await message.answer(
        text=menu.main_menu["text"],
        reply_markup=menu.main_menu["reply_markup"]
    )

@dp.callback_query(F.data == "return_to_main_menu")
async def return_to_main_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text=menu.main_menu["text"],
        reply_markup=menu.main_menu["reply_markup"]
    )

@dp.callback_query(F.data == "return_to_main_menu_as_answer")
async def return_to_main_menu(callback: CallbackQuery) -> None:
    await callback.message.answer(
        text=menu.main_menu["text"],
        reply_markup=menu.main_menu["reply_markup"]
    )
    await callback.message.delete()

@dp.callback_query(F.data == "info")
async def choose_formula(callback: CallbackQuery, state) -> None:
    data = await state.get_data()
    await callback.message.edit_text(
        text = "Данный бот представляет собой адскую хрень,\n"
               f"Выбрана формула для пола: {data.get("sex")}",
        reply_markup=menu.to_main_menu_kb
    )

@dp.callback_query(F.data == "formula")
async def choose_formula(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text = menu.choose_formula["text"],
        reply_markup=menu.choose_formula["reply_markup"]
    )

@dp.callback_query(F.data == "male")
async def set_sex_to_male(callback: CallbackQuery, state) -> None:
    await state.update_data(sex="Мужчина")
    await return_to_main_menu(callback)

@dp.callback_query(F.data == "female")
async def set_sex_to_female(callback, state) -> None:
    await state.update_data(sex="Женщина")
    await return_to_main_menu(callback)

@dp.callback_query(F.data == "calories")
async def calories_solving_start(callback, state) -> None:
    data = await state.get_data()
    if data.get("sex") is None:
        await state.update_data(sex="Мужчина")
    await state.set_state(UserState.age)
    await callback.message.answer("Введите свой возраст", reply_markup=menu.to_main_menu_kb)


@dp.message(UserState.age)
async def set_growth(message: types.message, state) -> None:
    await state.update_data(age = message.text)
    await state.set_state(UserState.growth)
    await message.answer("Введите свой рост", reply_markup=menu.to_main_menu_kb)

@dp.message(UserState.growth)
async def set_weight(message: types.message, state) -> None:
    await state.update_data(growth = message.text)
    await state.set_state(UserState.weight)
    await message.answer("Введите свой вес", reply_markup=menu.to_main_menu_kb)

@dp.message(UserState.weight)
async def send_calories(message: types.message, state) -> None:
    await state.update_data(weight = message.text)
    data = await state.get_data()
    await message.answer(f"Ваша норма калорий: {get_norm_of_calories(data)}",
                         reply_markup=menu.main_menu["reply_markup"])
    await state.clear()

def get_norm_of_calories(data: dict) -> float:
    if data["sex"] == "Мужчина":
        return 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5
    elif data["sex"] == "Женщина":
        return 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161
    else:
        return "Не совсем понятен ваш пол"


@dp.callback_query(F.data == "open_product_catalog")
async def open_catalog(callback: CallbackQuery, state) -> None:
    await state.set_state(UserState.product)
    product_to_buy = menu.products[0]
    await state.update_data(product=product_to_buy)
    await callback.message.edit_media(
        InputMediaPhoto(media=product_to_buy[1], caption=product_to_buy[0]),
        reply_markup=menu.product_catalog["reply_markup"]
    )

@dp.callback_query(F.data == "health+1")
async def open_catalog(callback: CallbackQuery, state) -> None:
    product_to_buy = menu.products[0]
    await state.update_data(product=product_to_buy[0])
    await callback.message.edit_media(
        InputMediaPhoto(media=product_to_buy[1], caption=product_to_buy[0]),
        reply_markup=menu.product_catalog["reply_markup"]
    )

@dp.callback_query(F.data == "health+10")
async def open_catalog(callback: CallbackQuery, state) -> None:
    product_to_buy = menu.products[1]
    await state.update_data(product=product_to_buy[0])
    await callback.message.edit_media(
        InputMediaPhoto(media=product_to_buy[1], caption=product_to_buy[0]),
        reply_markup=menu.product_catalog["reply_markup"]
    )

@dp.callback_query(F.data == "health+25")
async def open_catalog(callback: CallbackQuery, state) -> None:
    product_to_buy = menu.products[2]
    await state.update_data(product=product_to_buy[0])
    await callback.message.edit_media(
        InputMediaPhoto(media=product_to_buy[1], caption=product_to_buy[0]),
        reply_markup=menu.product_catalog["reply_markup"]
    )

@dp.callback_query(F.data == "health+50")
async def open_catalog(callback: CallbackQuery, state) -> None:
    product_to_buy = menu.products[3]
    await state.update_data(product=product_to_buy[0])
    await callback.message.edit_media(
        InputMediaPhoto(media=product_to_buy[1], caption=product_to_buy[0]),
        reply_markup=menu.product_catalog["reply_markup"]
    )

@dp.callback_query(F.data == "health+100")
async def open_catalog(callback: CallbackQuery, state) -> None:
    product_to_buy = menu.products[4]
    await state.update_data(product=product_to_buy[0])
    await callback.message.edit_media(
        InputMediaPhoto(media=product_to_buy[1], caption=product_to_buy[0]),
        reply_markup=menu.product_catalog["reply_markup"]
    )

@dp.callback_query(F.data == "invulnerability")
async def open_catalog(callback: CallbackQuery, state) -> None:
    product_to_buy = menu.products[5]
    await state.update_data(product=product_to_buy[0])
    await callback.message.edit_media(
        InputMediaPhoto(media=product_to_buy[1], caption=product_to_buy[0]),
        reply_markup=menu.product_catalog["reply_markup"]
    )

@dp.callback_query(F.data == "buy_product")
async def buy_product(callback: CallbackQuery, state) -> None:
    data = await state.get_data()
    await callback.message.answer(
        text=f"Продукт \"{data["product"]}\"{menu.product_selled["text"]}",
        reply_markup=menu.product_selled["reply_markup"]
    )

@dp.message()
async def any_other_message(message: types.Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())