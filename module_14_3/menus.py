from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types.input_file import FSInputFile


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
                                                   callback_data="male")],
                             [InlineKeyboardButton(text="Женская: 10 * вес + 6.25 * рост - 5 * возраст - 161",
                                                   callback_data="female")]
                             ])

choose_formula = {"text": "Выберите формулу:",
                  "reply_markup": formula_kb}

to_main_menu_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="В главное меню",
                                                   callback_data="return_to_main_menu")]
                             ])

product_catalog_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="Здоровье +1",
                                                   callback_data="health+1"),
                              InlineKeyboardButton(text="Здоровье +10",
                                                   callback_data="health+10"),
                              InlineKeyboardButton(text="Здоровье +25",
                                                   callback_data="health+25"),
                              InlineKeyboardButton(text="Здоровье +50",
                                                   callback_data="health+50"),
                              InlineKeyboardButton(text="Здоровье +100",
                                                   callback_data="health+100"),
                              InlineKeyboardButton(text="Неуязвимость",
                                                   callback_data="invulnerability")],
                             [InlineKeyboardButton(text="Купить",
                                                   callback_data="buy_product")],
                             [InlineKeyboardButton(text="В главное меню",
                                                   callback_data="return_to_main_menu_as_answer")]
                             ])

products = (("Здоровье +1", FSInputFile("Здоровье +1.jpg")),
            ("Здоровье +10", FSInputFile("Здоровье +10.jpg")),
            ("Здоровье +25", FSInputFile("Здоровье +25.jpg")),
            ("Здоровье +50", FSInputFile("Здоровье +50.jpg")),
            ("Здоровье +100", FSInputFile("Здоровье +100.jpg")),
            ("Неуязвимость", FSInputFile("Неуязвимость.jpg")))
product_catalog = {"text": products,
                  "reply_markup": product_catalog_kb}

product_selled_kb = InlineKeyboardMarkup(inline_keyboard=
                            [[InlineKeyboardButton(text="В каталог покупок",
                                                   callback_data="open_product_catalog")],
                             [InlineKeyboardButton(text="В главное меню",
                                                   callback_data="return_to_main_menu")]
                             ])
product_selled = {"text": " успешно куплен, хотите купить что-нибудь ещё?",
                  "reply_markup": product_selled_kb}