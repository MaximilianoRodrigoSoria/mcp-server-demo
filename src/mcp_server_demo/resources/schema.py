"""Resource: esquema de la base, para que el modelo sepa qué puede consultar."""

from __future__ import annotations

from mcp_server_demo.config import get_settings
from mcp_server_demo.db.connection import connect, query


def database_schema() -> str:
    """Devuelve el DDL de las tablas de la base como texto."""
    with connect(get_settings().db_file) as conn:
        rows = query(
            conn,
            "SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL ORDER BY name",
        )
    return "\n\n".join(r["sql"] for r in rows) or "(base vacía: corré scripts/seed_db.py)"
