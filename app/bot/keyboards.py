from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)


def main_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Каталог"), KeyboardButton(text="Корзина")],
            [KeyboardButton(text="Оформить"), KeyboardButton(text="Помощь")],
        ],
        resize_keyboard=True,
    )


def categories_kb(categories: list[str]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=cat, callback_data=f"cat:{cat}")]
        for cat in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_kb(category: str, products: list[tuple[int, str]]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=title, callback_data=f"p:{product_id}")]
        for product_id, title in products
    ]
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="cats")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def product_card_kb(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="➕ В корзину", callback_data=f"add:{product_id}"),
                InlineKeyboardButton(text="Корзина", callback_data="cart"),
            ],
            [InlineKeyboardButton(text="⬅️ Каталог", callback_data="cats")],
        ]
    )


def cart_kb(item_ids: list[int]) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    for product_id in item_ids:
        rows.append(
            [
                InlineKeyboardButton(text="➖", callback_data=f"dec:{product_id}"),
                InlineKeyboardButton(text="➕", callback_data=f"inc:{product_id}"),
                InlineKeyboardButton(text="❌", callback_data=f"rm:{product_id}"),
            ]
        )
    rows.append(
        [
            InlineKeyboardButton(text="Очистить", callback_data="clr"),
            InlineKeyboardButton(text="Оформить", callback_data="chk"),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=rows)


def checkout_request_contact_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отправить телефон", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def back_to_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Меню")]], resize_keyboard=True
    )
