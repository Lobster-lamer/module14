from aiogram import types, F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.command import CommandStart
from aiogram.types import  CallbackQuery, Message
import menus as menu
from menus import UserSex

main_menu_router = Router()

class UserState(StatesGroup):
    sex = State()
    age = State()
    growth = State()
    weight = State()
    options_answer_message: Message = None


@main_menu_router.message(CommandStart())
async def cmd_start(message: types.Message, state) -> None:
    UserState.options_answer_message = message
    await state.set_state(UserState.sex)
    await message.answer(
        text=menu.main_menu["text"],
        reply_markup=menu.main_menu["reply_markup"]
    )

@main_menu_router.callback_query(F.data == "return_to_main_menu")
async def return_to_main_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text=menu.main_menu["text"],
        reply_markup=menu.main_menu["reply_markup"]
    )

@main_menu_router.callback_query(F.data == "return_to_main_menu_as_answer")
async def return_to_main_menu_as_answer(callback: CallbackQuery) -> None:
    await callback.message.answer(
        text=menu.main_menu["text"],
        reply_markup=menu.main_menu["reply_markup"]
    )
    await callback.message.delete()

@main_menu_router.callback_query(F.data == "info")
async def choose_formula(callback: CallbackQuery, state) -> None:
    data = await state.get_data()
    await callback.message.edit_text(
        text = "Данный бот представляет собой адскую хрень,\n"
               f"Выбрана формула для пола: {data.get("sex").value}",
        reply_markup=menu.to_main_menu_kb
    )

@main_menu_router.callback_query(F.data == "formula")
async def choose_formula(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text = menu.choose_formula["text"],
        reply_markup=menu.choose_formula["reply_markup"]
    )

@main_menu_router.callback_query(menu.UserSex.filter(F.usex))
async def set_sex_to_male(callback: CallbackQuery, state, callback_data: UserSex) -> None:
    await state.update_data(sex=callback_data.usex)
    await return_to_main_menu(callback)
