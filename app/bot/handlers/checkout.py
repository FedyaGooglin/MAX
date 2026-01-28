from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards import checkout_request_contact_kb, main_menu_kb
from app.storage.repo import Repo

router = Router()
repo = Repo()


class CheckoutState(StatesGroup):
    waiting_phone = State()
    waiting_address = State()


async def start_checkout(message: Message, state: FSMContext, user_id: int) -> None:
    items = repo.get_cart_items(user_id)
    if not items:
        await message.answer("Корзина пуста.")
        return
    await state.set_state(CheckoutState.waiting_phone)
    await message.answer(
        "Пожалуйста, отправьте телефон:",
        reply_markup=checkout_request_contact_kb(),
    )


@router.message(lambda msg: msg.text and msg.text.lower() == "оформить")
async def checkout_from_menu(message: Message, state: FSMContext) -> None:
    await start_checkout(message, state, message.from_user.id)


@router.callback_query(lambda call: call.data == "chk")
async def checkout_from_cart(call: CallbackQuery, state: FSMContext) -> None:
    message = call.message
    if message is None:
        await call.answer()
        return
    await call.answer()
    await start_checkout(message, state, call.from_user.id)


@router.message(CheckoutState.waiting_phone)
async def checkout_phone(message: Message, state: FSMContext) -> None:
    if not message.contact or not message.contact.phone_number:
        await message.answer("Нажмите кнопку для отправки телефона.")
        return
    await state.update_data(phone=message.contact.phone_number)
    await state.set_state(CheckoutState.waiting_address)
    await message.answer(
        "Введите адрес доставки текстом:",
        reply_markup=main_menu_kb(),
    )


@router.message(CheckoutState.waiting_address)
async def checkout_address(message: Message, state: FSMContext) -> None:
    address_text = (message.text or "").strip()
    if not address_text:
        await message.answer("Пожалуйста, введите адрес текстом.")
        return
    data = await state.get_data()
    phone = data.get("phone", "")
    order_id = repo.create_order(message.from_user.id, phone, address_text)
    await state.clear()
    if order_id is None:
        await message.answer("Корзина пуста, заказ не создан.")
        return
    await message.answer(
        f"Спасибо! Заказ №{order_id} создан со статусом NEW.",
        reply_markup=main_menu_kb(),
    )
