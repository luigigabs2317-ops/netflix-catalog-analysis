"""Executa todos os arquivos de sql/ e salva os resultados em outputs/*.csv.

Uso:
    python src/run_queries.py
"""
import sqlite3
from pathlib import Path

import pandas as pd

DB_PATH = Path("data/netflix.db")
SQL_DIR = Path("sql")
OUT_DIR = Path("outputs")


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        for sql_file in sorted(SQL_DIR.glob("*.sql")):
            result = pd.read_sql_query(sql_file.read_text(encoding="utf-8"), conn)
            result.to_csv(OUT_DIR / f"{sql_file.stem}.csv", index=False)
            print(f"\n=== {sql_file.name} ({len(result)} linhas) ===")
            print(result.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
