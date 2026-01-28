# Telegram-магазин (aiogram)

MVP Telegram-бот магазина на **aiogram** (Python 3.11+), запуск в режиме **long polling**.

## Возможности
- Каталог товаров: категории → список → карточка товара
- Корзина: добавить/убавить, удалить позицию, очистить, итоговая сумма
- Оформление заказа: телефон + адрес (статус NEW)
- Админ-команды: `/seed`, `/orders`

## Установка
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Настройка окружения
Создайте `.env` по примеру `.env.example` (файл подхватывается автоматически):
```bash
TOKEN=your_bot_token
DB_PATH=data/app.db
```

## Запуск бота
```bash
python -m app.main
```

## Засеять базу тестовыми товарами
```bash
# в чате с ботом
/seed
```

## Линтер и тесты
```bash
ruff check app tests
pytest -q
```
