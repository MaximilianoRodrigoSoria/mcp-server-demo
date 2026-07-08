"""Tools de base de datos expuestas al LLM. Entradas validadas, SQL parametrizado."""

from __future__ import annotations

from mcp_server_demo.config import get_settings
from mcp_server_demo.db.connection import connect, query


def search_customers(name: str, limit: int = 10) -> list[dict]:
    """Busca clientes cuyo nombre contenga `name` (case-insensitive)."""
    name = (name or "").strip()
    if not name:
        return []
    limit = max(1, min(int(limit), 50))
    with connect(get_settings().db_file) as conn:
        return query(
            conn,
            "SELECT id, name, email FROM customers WHERE name LIKE ? ORDER BY name LIMIT ?",
            (f"%{name}%", limit),
        )


def get_order_by_id(order_id: int) -> dict | None:
    """Devuelve un pedido por id, o None si no existe."""
    with connect(get_settings().db_file) as conn:
        rows = query(
            conn,
            "SELECT o.id, o.customer_id, c.name AS customer, o.total, o.status "
            "FROM orders o JOIN customers c ON c.id = o.customer_id WHERE o.id = ?",
            (int(order_id),),
        )
    return rows[0] if rows else None
