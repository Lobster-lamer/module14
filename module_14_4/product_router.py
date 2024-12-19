from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import  CallbackQuery, InputMediaPhoto
from aiogram.types.input_file import FSInputFile
import menus as menu
import crud_functions as cf


class ProductMenu(StatesGroup):
    product = State()
    product_list_page = State()
    product_list_page_limit = State()


product_db = cf.DatabaseHandler("Products")
product_list = product_db.get_all_products_as_dicts()

product_buy_router = Router()

@product_buy_router.callback_query(F.data == "open_product_catalog")
async def first_open_catalog(callback: CallbackQuery, state) -> None:
    await state.set_state(ProductMenu.product)
    await state.set_state(ProductMenu.product_list_page)
    await state.set_state(ProductMenu.product_list_page_limit)
    product_to_buy = product_list[0]
    product_list_page_limit = 4
    await state.update_data(product=product_to_buy["title"])
    await state.update_data(product_list_page=0)
    await state.update_data(product_list_page_limit=product_list_page_limit)
    await callback.message.edit_media(
        InputMediaPhoto(media=FSInputFile(f"images/{product_to_buy["title"]}.jpg"),
                        caption=f"{product_to_buy["title"]}\n"
                                f"{product_to_buy["description"]}\n"
                                f"Цена: {product_to_buy["price"]}"),
                        reply_markup=menu.product_catalog["reply_markup"](page=0,
                                                                          product_page_limit=product_list_page_limit)
    )

@product_buy_router.callback_query(F.data == "previous_page")
async def set_previous_page(callback: CallbackQuery, state):
    data = await state.get_data()
    await state.update_data(product_list_page=data["product_list_page"] - 1)
    await open_page(callback, state)


@product_buy_router.callback_query(F.data == "next_page")
async def set_next_page(callback: CallbackQuery, state):
    data = await state.get_data()
    await state.update_data(product_list_page=data["product_list_page"] + 1)
    await open_page(callback, state)

async def open_page(callback, state):
    data = await state.get_data()
    product_to_buy = product_list[data["product_list_page"] * data["product_list_page_limit"]]
    await state.update_data(product=product_to_buy["title"])
    await callback.message.edit_media(
        InputMediaPhoto(media=FSInputFile(f"images/{product_to_buy["title"]}.jpg"),
                        caption=f"{product_to_buy["title"]}\n"
                                f"{product_to_buy["description"]}\n"
                                f"Цена: {product_to_buy["price"]}"),
                        reply_markup=menu.product_catalog["reply_markup"](page=data["product_list_page"],
                                                            product_page_limit=data["product_list_page_limit"])
    )

@product_buy_router.callback_query(menu.ProductNumber.filter(F.number))
async def choose_product(callback: CallbackQuery, state, callback_data: menu.ProductNumber) -> None:
    product_to_buy = product_list[callback_data.number-1]
    data = await state.get_data()
    await state.update_data(product=product_to_buy["title"])
    await callback.message.edit_media(
        InputMediaPhoto(media=FSInputFile(f"images/{product_to_buy["title"]}.jpg"),
                        caption=f"{product_to_buy["title"]}\n"
                                f"{product_to_buy["description"]}\n"
                                f"Цена: {product_to_buy["price"]}"),
                        reply_markup=menu.product_catalog["reply_markup"](page=data["product_list_page"],
                                                            product_page_limit=data["product_list_page_limit"])
    )

@product_buy_router.callback_query(F.data == "buy_product")
async def buy_product(callback: CallbackQuery, state) -> None:
    data = await state.get_data()
    await callback.message.answer(
        text=f"Продукт \"{data["product"]}\"{menu.product_selled["text"]}",
        reply_markup=menu.product_selled["reply_markup"]
    )
    await callback.message.delete()
    await state.clear()
