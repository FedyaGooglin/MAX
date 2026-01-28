from aiogram import Router
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import cart_kb
from app.storage.repo import Repo

router = Router()
repo = Repo()


def render_cart(user_id: int) -> tuple[str, list[int]]:
    items = repo.get_cart_items(user_id)
    if not items:
        return "Корзина пуста.", []
    lines = ["Корзина:"]
    item_ids: list[int] = []
    total = 0
    for item in items:
        line_total = item.price * item.qty
        total += line_total
        lines.append(f"{item.title} — {item.qty} шт. x {item.price} ₽ = {line_total} ₽")
        item_ids.append(item.product_id)
    lines.append(f"Итого: {total} ₽")
    return "\n".join(lines), item_ids


@router.message(lambda msg: msg.text and msg.text.lower() == "корзина")
async def cart_view(message: Message) -> None:
    text, item_ids = render_cart(message.from_user.id)
    if not item_ids:
        await message.answer(text)
        return
    await message.answer(text, reply_markup=cart_kb(item_ids))


@router.callback_query(lambda call: call.data == "cart")
async def cart_view_inline(call: CallbackQuery) -> None:
    text, item_ids = render_cart(call.from_user.id)
    if not item_ids:
        await call.message.edit_text(text)
        await call.answer()
        return
    await call.message.edit_text(text, reply_markup=cart_kb(item_ids))
    await call.answer()


@router.callback_query(lambda call: call.data and call.data.startswith("inc:"))
async def cart_inc(call: CallbackQuery) -> None:
    product_id = int(call.data.split(":", 1)[1])
    repo.add_to_cart(call.from_user.id, product_id, 1)
    await cart_view_inline(call)


@router.callback_query(lambda call: call.data and call.data.startswith("dec:"))
async def cart_dec(call: CallbackQuery) -> None:
    product_id = int(call.data.split(":", 1)[1])
    repo.add_to_cart(call.from_user.id, product_id, -1)
    await cart_view_inline(call)


@router.callback_query(lambda call: call.data and call.data.startswith("rm:"))
async def cart_remove(call: CallbackQuery) -> None:
    product_id = int(call.data.split(":", 1)[1])
    repo.remove_from_cart(call.from_user.id, product_id)
    await cart_view_inline(call)


@router.callback_query(lambda call: call.data == "clr")
async def cart_clear(call: CallbackQuery) -> None:
    repo.clear_cart(call.from_user.id)
    await cart_view_inline(call)
