"""Tests de las tools de DB contra una base temporal sembrada."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from mcp_server_demo import config
from mcp_server_demo.tools import db_tools


@pytest.fixture
def seeded_db(tmp_path, monkeypatch):
    db = tmp_path / "demo.db"
    sql = (config.ROOT_DIR / "data" / "seed.sql").read_text(encoding="utf-8")
    conn = sqlite3.connect(db)
    conn.executescript(sql)
    conn.commit()
    conn.close()
    monkeypatch.setattr(config, "get_settings", lambda: config.Settings(_env_file=None, DB_PATH=str(db)))
    # db_tools importó get_settings por nombre: apuntarlo también
    monkeypatch.setattr(db_tools, "get_settings", config.get_settings)
    return db


def test_search_customers(seeded_db):
    res = db_tools.search_customers("a")
    assert any(c["name"] == "Ada Lovelace" for c in res)


def test_search_customers_vacio(seeded_db):
    assert db_tools.search_customers("") == []


def test_get_order_by_id(seeded_db):
    order = db_tools.get_order_by_id(102)
    assert order and order["customer"] == "Alan Turing" and order["status"] == "paid"


def test_get_order_inexistente(seeded_db):
    assert db_tools.get_order_by_id(9999) is None
