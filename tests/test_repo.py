from pathlib import Path

from app.storage.db import init_db
from app.storage.repo import Repo


def create_repo(tmp_path: Path) -> Repo:
    db_path = tmp_path / "test.db"
    init_db(db_path)
    return Repo(db_path)


def test_seed_and_list_categories(tmp_path: Path) -> None:
    repo = create_repo(tmp_path)
    repo.seed_products()
    categories = repo.list_categories()
    assert set(categories) == {"Напитки", "Выпечка", "Еда"}


def test_add_to_cart_and_get_items(tmp_path: Path) -> None:
    repo = create_repo(tmp_path)
    repo.seed_products()
    repo.add_to_cart(1, 1, 2)
    items = repo.get_cart_items(1)
    assert len(items) == 1
    assert items[0].qty == 2


def test_cart_decrease_removes_item(tmp_path: Path) -> None:
    repo = create_repo(tmp_path)
    repo.seed_products()
    repo.add_to_cart(1, 1, 1)
    repo.add_to_cart(1, 1, -1)
    items = repo.get_cart_items(1)
    assert items == []


def test_create_order_clears_cart(tmp_path: Path) -> None:
    repo = create_repo(tmp_path)
    repo.seed_products()
    repo.add_to_cart(1, 1, 2)
    order_id = repo.create_order(1, "+79990000000", "Москва")
    assert order_id is not None
    items = repo.get_cart_items(1)
    assert items == []


def test_recent_orders_returns_latest(tmp_path: Path) -> None:
    repo = create_repo(tmp_path)
    repo.seed_products()
    repo.add_to_cart(1, 1, 1)
    repo.create_order(1, "+79990000001", "Адрес 1")
    repo.add_to_cart(2, 2, 1)
    repo.create_order(2, "+79990000002", "Адрес 2")
    orders = repo.get_recent_orders(1)
    assert len(orders) == 1
    assert orders[0].user_id == 2
