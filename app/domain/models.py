from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    id: int
    title: str
    price: int
    in_stock: int
    category: str


@dataclass(slots=True)
class CartItem:
    product_id: int
    title: str
    price: int
    qty: int


@dataclass(slots=True)
class Order:
    id: int
    user_id: int
    total: int
    phone: str
    address_text: str
    status: str
    created_at: str
