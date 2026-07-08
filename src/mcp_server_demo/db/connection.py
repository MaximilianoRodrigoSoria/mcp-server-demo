"""Acceso a SQLite con queries SIEMPRE parametrizadas (anti inyección)."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


@contextmanager
def connect(db_path: str | Path) -> Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def query(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[dict]:
    """Ejecuta un SELECT parametrizado y devuelve filas como dicts."""
    cur = conn.execute(sql, params)
    return [dict(row) for row in cur.fetchall()]
