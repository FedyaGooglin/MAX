from aiogram import Dispatcher

from app.bot.handlers import admin, cart, catalog, checkout, start


def setup_router(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(catalog.router)
    dp.include_router(cart.router)
    dp.include_router(checkout.router)
    dp.include_router(admin.router)
