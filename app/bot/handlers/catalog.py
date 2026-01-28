from aiogram import Router
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import categories_kb, product_card_kb, products_kb
from app.storage.repo import Repo

router = Router()
repo = Repo()


@router.message(lambda msg: msg.text and msg.text.lower() == "каталог")
async def catalog_menu(message: Message) -> None:
    categories = repo.list_categories()
    if not categories:
        await message.answer("Каталог пуст.")
        return
    await message.answer("Категории:", reply_markup=categories_kb(categories))


@router.callback_query(lambda call: call.data == "cats")
async def catalog_categories(call: CallbackQuery) -> None:
    categories = repo.list_categories()
    if not categories:
        await call.message.edit_text("Каталог пуст.")
        await call.answer()
        return
    await call.message.edit_text("Категории:", reply_markup=categories_kb(categories))
    await call.answer()


@router.callback_query(lambda call: call.data and call.data.startswith("cat:"))
async def catalog_products(call: CallbackQuery) -> None:
    category = call.data.split(":", 1)[1]
    products = repo.list_products(category)
    if not products:
        await call.message.edit_text("В этой категории нет товаров.")
        await call.answer()
        return
    await call.message.edit_text(
        f"Товары в категории: {category}",
        reply_markup=products_kb(category, products),
    )
    await call.answer()


@router.callback_query(lambda call: call.data and call.data.startswith("p:"))
async def product_card(call: CallbackQuery) -> None:
    product_id = int(call.data.split(":", 1)[1])
    product = repo.get_product(product_id)
    if not product:
        await call.message.edit_text("Товар не найден.")
        await call.answer()
        return
    text = (
        f"{product.title}\n"
        f"Цена: {product.price} ₽\n"
        f"В наличии: {product.in_stock}"
    )
    await call.message.edit_text(text, reply_markup=product_card_kb(product_id))
    await call.answer()


@router.callback_query(lambda call: call.data and call.data.startswith("add:"))
async def add_to_cart(call: CallbackQuery) -> None:
    product_id = int(call.data.split(":", 1)[1])
    repo.add_to_cart(call.from_user.id, product_id, 1)
    await call.answer("Добавлено в корзину")
