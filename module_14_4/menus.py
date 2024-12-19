from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types.input_file import FSInputFile
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from enum import Enum
from pprint import pprint

class ProductNumber(CallbackData, prefix="pn"):
    number: int


class Sex(str, Enum):
    male = "Мужчина"
    female = "Женщина"


class UserSex(CallbackData, prefix="sex"):
    usex: Sex


main_menu_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="Рассчитать норму калорий",
                                                   callback_data="calories"),
                              InlineKeyboardButton(text="Выбрать формулу расчёта",
                                                   callback_data="formula")],
                             [InlineKeyboardButton(text="Купить",
                                                   callback_data="open_product_catalog")],
                             [InlineKeyboardButton(text="Информация",
                                                   callback_data="info")]
                             ])

main_menu = {"text": "Привет! Я бот помогающий твоему здоровью.",
             "reply_markup": main_menu_kb}

formula_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="Мужская: 10 * вес + 6.25 * рост - 5 * возраст + 5",
                                                   callback_data=UserSex(usex=Sex.male).pack())],
                             [InlineKeyboardButton(text="Женская: 10 * вес + 6.25 * рост - 5 * возраст - 161",
                                                   callback_data=UserSex(usex=Sex.female).pack())]
                             ])

choose_formula = {"text": "Выберите формулу:",
                  "reply_markup": formula_kb}

to_main_menu_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="В главное меню",
                                                   callback_data="return_to_main_menu")]
                             ])


products = ({"title":"Здоровье +1",
             "description": "Добавляет 1 единицу здоровья, хотя обычно это ловушка",
             "price": 1,
             "image_path": FSInputFile("Здоровье +1.jpg")},
            {"title":"Здоровье +10",
             "description": "Добавляет 10 единиц здоровья",
             "price": 10,
             "image_path": FSInputFile("Здоровье +10.jpg")},
            {"title":"Здоровье +25",
             "description": "Добавляет 10 единиц здоровья",
             "price": 25,
             "image_path": FSInputFile("Здоровье +25.jpg")},
            {"title":"Здоровье +50",
             "description": "Добавляет 10 единиц здоровья",
             "price": 50,
             "image_path": FSInputFile("Здоровье +50.jpg")},
            {"title":"Здоровье +100",
             "description": "Добавляет 10 единиц здоровья",
             "price": 100,
             "image_path": FSInputFile("Здоровье +100.jpg")},
            {"title":"Неуязвимость",
             "description": "Делает на время неуязвимым (на случай косяка перед девушкой)",
             "price": 1000,
             "image_path": FSInputFile("Неуязвимость.jpg")})


product_menu_standart_buttons = (InlineKeyboardButton(text="Купить",
                                                    callback_data = "buy_product"),
                                 InlineKeyboardButton(text="В главное меню",
                                                    callback_data="return_to_main_menu_as_answer"))

def get_last_page_number(products_, product_page_limit):
    products_len = len(products_)
    if products_len % product_page_limit == 0:
        last_page_ = products_len // product_page_limit
    else:
        last_page_ = products_len // product_page_limit + 1
    return last_page_

def build_product_list(products_, product_page_limit, page):
    product_list = []
    first_product_number = page * product_page_limit
    if product_page_limit * (page + 1) > len(products_):
        product_page_limit = len(products_) % product_page_limit
    for product_number in range(first_product_number, first_product_number + product_page_limit):
        product_list.append(InlineKeyboardButton(text=f"{products_[product_number]["title"]}",
                                                callback_data=ProductNumber(number=product_number+1).pack()))
    return product_list, product_page_limit

def build_pagination_buttons(products_, product_page_limit, page):
    pagination_buttons = []
    button_prev = InlineKeyboardButton(text="<<",
                                       callback_data="previous_page")
    button_next = InlineKeyboardButton(text=">>",
                                       callback_data="next_page")
    if page != 0:
        pagination_buttons.append(button_prev)
    pagination_buttons.append(InlineKeyboardButton(text=f"Страница {page + 1}/"
                                                        f"{get_last_page_number(products_, product_page_limit)}",
                                               callback_data="None"))
    if (page + 1) != get_last_page_number(products_, product_page_limit):
        pagination_buttons.append(button_next)
    page_change_buttons_len = len(pagination_buttons)
    return pagination_buttons, page_change_buttons_len

def build_product_menu(products_ = products, product_page_limit: int = 3, page: int=0,
                       standart_buttons = product_menu_standart_buttons):
    product_catalog_kb_ = InlineKeyboardBuilder()

    product_buttons, upd_product_page_limit = build_product_list(products_, product_page_limit, page)
    for product_button in product_buttons:
        product_catalog_kb_.add(product_button)

    pagination_buttons, page_change_buttons_len = build_pagination_buttons(products_, product_page_limit, page)
    for button in pagination_buttons:
        product_catalog_kb_.add(button)

    for button in standart_buttons:
        product_catalog_kb_.add(button)

    product_catalog_kb_.adjust(upd_product_page_limit, page_change_buttons_len, 1, 1)

    return InlineKeyboardMarkup(inline_keyboard=product_catalog_kb_.export())

product_catalog = {"text": products,
                  "reply_markup": build_product_menu}


product_selled_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="В каталог покупок",
                                                   callback_data="open_product_catalog")],
                             [InlineKeyboardButton(text="В главное меню",
                                                   callback_data="return_to_main_menu")]
                             ])
product_selled = {"text": " успешно куплен, хотите купить что-нибудь ещё?",
                  "reply_markup": product_selled_kb}


if __name__ == "__main__":
    pprint(product_catalog["text"])