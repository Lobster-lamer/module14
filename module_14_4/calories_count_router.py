from aiogram import types, F, Router
import menus as menu
from main_menu_router import UserState


calories_count_router = Router()

@calories_count_router.callback_query(F.data == "calories")
async def calories_solving_start(callback, state) -> None:
    data = await state.get_data()
    if data.get("sex") is None:
        await state.update_data(sex="Мужчина")
    await state.set_state(UserState.age)
    await callback.message.answer("Введите свой возраст", reply_markup=menu.to_main_menu_kb)
    await callback.message.delete()


@calories_count_router.message(UserState.age)
async def set_growth(message: types.message, state) -> None:
    await state.update_data(age = message.text)
    await state.set_state(UserState.growth)
    await message.answer("Введите свой рост", reply_markup=menu.to_main_menu_kb)

@calories_count_router.message(UserState.growth)
async def set_weight(message: types.message, state) -> None:
    await state.update_data(growth = message.text)
    await state.set_state(UserState.weight)
    await message.answer("Введите свой вес", reply_markup=menu.to_main_menu_kb)

@calories_count_router.message(UserState.weight)
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
