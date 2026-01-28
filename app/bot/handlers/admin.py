from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.storage.repo import Repo

router = Router()
repo = Repo()


@router.message(Command("seed"))
async def seed_handler(message: Message) -> None:
    count = repo.seed_products()
    await message.answer(f"Добавлено товаров: {count}")


@router.message(Command("orders"))
async def orders_handler(message: Message) -> None:
    orders = repo.get_recent_orders(10)
    if not orders:
        await message.answer("Заказов пока нет.")
        return
    lines = ["Последние заказы:"]
    for order in orders:
        lines.append(
            f"#{order.id} | {order.total} ₽ | {order.status} | {order.created_at}"
        )
    await message.answer("\n".join(lines))
