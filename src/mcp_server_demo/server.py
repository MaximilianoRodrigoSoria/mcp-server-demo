"""Servidor MCP (FastMCP): registra tools y un resource.

Ejecutar por stdio (para Claude Desktop / MCP Inspector):
    python -m mcp_server_demo.server
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from mcp_server_demo.resources.schema import database_schema
from mcp_server_demo.tools.api_tools import get_weather as _get_weather
from mcp_server_demo.tools.db_tools import get_order_by_id as _get_order_by_id
from mcp_server_demo.tools.db_tools import search_customers as _search_customers

mcp = FastMCP("mcp-server-demo")


@mcp.tool()
def search_customers(name: str, limit: int = 10) -> list[dict]:
    """Busca clientes por nombre (coincidencia parcial)."""
    return _search_customers(name, limit)


@mcp.tool()
def get_order_by_id(order_id: int) -> dict | None:
    """Devuelve un pedido por su id (incluye el cliente)."""
    return _get_order_by_id(order_id)


@mcp.tool()
def get_weather(city: str) -> dict:
    """Clima actual de una ciudad (Open-Meteo, sin API key)."""
    return _get_weather(city)


@mcp.resource("schema://database")
def db_schema() -> str:
    """Esquema (DDL) de la base de datos."""
    return database_schema()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
