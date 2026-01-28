import os
import sqlite3
from datetime import datetime
from pathlib import Path

from app.domain.models import CartItem, Order, Product
from app.storage.db import get_connection


class Repo:
    def __init__(self, db_path: Path | None = None) -> None:
        if db_path is None:
            db_path = Path(os.getenv("DB_PATH", "data/app.db"))
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        return get_connection(self.db_path)

    def list_categories(self) -> list[str]:
        conn = self._connect()
        rows = conn.execute(
            "SELECT DISTINCT category FROM products ORDER BY category"
        ).fetchall()
        conn.close()
        return [row["category"] for row in rows]

    def list_products(self, category: str) -> list[tuple[int, str]]:
        conn = self._connect()
        rows = conn.execute(
            "SELECT id, title FROM products WHERE category = ? ORDER BY id",
            (category,),
        ).fetchall()
        conn.close()
        return [(row["id"], row["title"]) for row in rows]

    def get_product(self, product_id: int) -> Product | None:
        conn = self._connect()
        row = conn.execute(
            "SELECT id, title, price, in_stock, category FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return Product(
            id=row["id"],
            title=row["title"],
            price=row["price"],
            in_stock=row["in_stock"],
            category=row["category"],
        )

    def add_to_cart(self, user_id: int, product_id: int, delta: int) -> None:
        conn = self._connect()
        with conn:
            row = conn.execute(
                "SELECT qty FROM cart_items WHERE user_id = ? AND product_id = ?",
                (user_id, product_id),
            ).fetchone()
            if row is None:
                if delta > 0:
                    conn.execute(
                        "INSERT INTO cart_items (user_id, product_id, qty) VALUES (?, ?, ?)",
                        (user_id, product_id, delta),
                    )
            else:
                new_qty = row["qty"] + delta
                if new_qty <= 0:
                    conn.execute(
                        "DELETE FROM cart_items WHERE user_id = ? AND product_id = ?",
                        (user_id, product_id),
                    )
                else:
                    conn.execute(
                        "UPDATE cart_items SET qty = ? WHERE user_id = ? AND product_id = ?",
                        (new_qty, user_id, product_id),
                    )
        conn.close()

    def get_cart_items(self, user_id: int) -> list[CartItem]:
        conn = self._connect()
        rows = conn.execute(
            """
            SELECT c.product_id, p.title, p.price, c.qty
            FROM cart_items c
            JOIN products p ON p.id = c.product_id
            WHERE c.user_id = ?
            ORDER BY p.title
            """,
            (user_id,),
        ).fetchall()
        conn.close()
        return [
            CartItem(
                product_id=row["product_id"],
                title=row["title"],
                price=row["price"],
                qty=row["qty"],
            )
            for row in rows
        ]

    def remove_from_cart(self, user_id: int, product_id: int) -> None:
        conn = self._connect()
        with conn:
            conn.execute(
                "DELETE FROM cart_items WHERE user_id = ? AND product_id = ?",
                (user_id, product_id),
            )
        conn.close()

    def clear_cart(self, user_id: int) -> None:
        conn = self._connect()
        with conn:
            conn.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
        conn.close()

    def create_order(self, user_id: int, phone: str, address_text: str) -> int | None:
        conn = self._connect()
        rows = conn.execute(
            """
            SELECT c.product_id, c.qty, p.price
            FROM cart_items c
            JOIN products p ON p.id = c.product_id
            WHERE c.user_id = ?
            """,
            (user_id,),
        ).fetchall()
        if not rows:
            conn.close()
            return None
        total = sum(row["price"] * row["qty"] for row in rows)
        created_at = datetime.utcnow().isoformat()
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO orders (user_id, total, phone, address_text, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, total, phone, address_text, "NEW", created_at),
            )
            order_id = cursor.lastrowid
            conn.executemany(
                """
                INSERT INTO order_items (order_id, product_id, qty, price)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (order_id, row["product_id"], row["qty"], row["price"])
                    for row in rows
                ],
            )
            conn.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
        conn.close()
        return int(order_id)

    def get_recent_orders(self, limit: int) -> list[Order]:
        conn = self._connect()
        rows = conn.execute(
            """
            SELECT id, user_id, total, phone, address_text, status, created_at
            FROM orders
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        conn.close()
        return [
            Order(
                id=row["id"],
                user_id=row["user_id"],
                total=row["total"],
                phone=row["phone"],
                address_text=row["address_text"],
                status=row["status"],
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def seed_products(self) -> int:
        items = [
            ("Кофе", 250, 50, "Напитки"),
            ("Чай", 180, 40, "Напитки"),
            ("Круассан", 120, 30, "Выпечка"),
            ("Пирожок", 90, 25, "Выпечка"),
            ("Сэндвич", 300, 20, "Еда"),
        ]
        conn = self._connect()
        with conn:
            conn.executemany(
                "INSERT INTO products (title, price, in_stock, category) VALUES (?, ?, ?, ?)",
                items,
            )
        conn.close()
        return len(items)
