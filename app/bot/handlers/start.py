from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.bot.keyboards import main_menu_kb

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "Добро пожаловать в магазин! Выберите действие:",
        reply_markup=main_menu_kb(),
    )


@router.message(lambda msg: msg.text and msg.text.lower() == "меню")
async def menu_handler(message: Message) -> None:
    await message.answer("Главное меню:", reply_markup=main_menu_kb())


@router.message(lambda msg: msg.text and msg.text.lower() == "помощь")
async def help_handler(message: Message) -> None:
    await message.answer(
        "Команды:\n"
        "/start — главное меню\n"
        "Каталог — просмотр товаров\n"
        "Корзина — управление корзиной\n"
        "Оформить — оформить заказ"
    )
