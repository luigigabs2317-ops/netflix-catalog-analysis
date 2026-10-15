"""Carrega os CSVs tratados em um banco SQLite e cria índices.

Uso:
    python src/load_to_sqlite.py
"""
import sqlite3
from pathlib import Path

import pandas as pd

PROCESSED = Path("data/processed")
DB_PATH = Path("data/netflix.db")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        titles = pd.read_csv(
            PROCESSED / "titles.csv",
            parse_dates=["date_added"],
            dtype={"year_added": "Int64", "month_added": "Int64", "release_gap": "Int64"},
        )
        titles["date_added"] = titles["date_added"].dt.strftime("%Y-%m-%d")
        titles.to_sql("titles", conn, if_exists="replace", index=False)

        for name in ("genres", "countries"):
            pd.read_csv(PROCESSED / f"{name}.csv").to_sql(
                name, conn, if_exists="replace", index=False
            )

        conn.executescript(
            """
            CREATE INDEX IF NOT EXISTS idx_titles_show_id ON titles(show_id);
            CREATE INDEX IF NOT EXISTS idx_genres_show_id ON genres(show_id);
            CREATE INDEX IF NOT EXISTS idx_countries_show_id ON countries(show_id);
            """
        )
        for table in ("titles", "genres", "countries"):
            n = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"{table}: {n} linhas")
    print(f"Banco criado em {DB_PATH}")


if __name__ == "__main__":
    main()
