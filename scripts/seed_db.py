"""Crea data/demo.db a partir de data/seed.sql (idempotente: recrea desde cero)."""

from __future__ import annotations

import sqlite3

from mcp_server_demo.config import ROOT_DIR, get_settings


def main() -> int:
    db = get_settings().db_file
    db.parent.mkdir(parents=True, exist_ok=True)
    sql = (ROOT_DIR / "data" / "seed.sql").read_text(encoding="utf-8")
    conn = sqlite3.connect(str(db))
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()
    print(f"Base sembrada en {db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
