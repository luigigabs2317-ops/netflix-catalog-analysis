"""Gera gráficos estáticos para o README (docs/img/*.png).

Uso:
    python src/charts.py
"""
import sqlite3
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DB_PATH = Path("data/netflix.db")
IMG_DIR = Path("docs/img")
RED = "#E50914"
GRAY = "#564d4d"


def query(conn, sql: str) -> pd.DataFrame:
    return pd.read_sql_query(sql, conn)


def chart_additions_by_year(conn) -> None:
    df = query(conn, """
        SELECT year_added AS ano, type, COUNT(*) AS titulos
        FROM titles WHERE year_added IS NOT NULL
        GROUP BY year_added, type ORDER BY year_added
    """).pivot(index="ano", columns="type", values="titulos").fillna(0)
    ax = df.plot(kind="bar", stacked=True, color=[RED, GRAY], figsize=(10, 5))
    ax.set_title("Títulos adicionados ao catálogo por ano")
    ax.set_xlabel("Ano de entrada no catálogo")
    ax.set_ylabel("Quantidade de títulos")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "01_adicoes_por_ano.png", dpi=150)
    plt.close()


def chart_top_countries(conn) -> None:
    df = query(conn, """
        SELECT country AS pais, COUNT(DISTINCT show_id) AS titulos
        FROM countries WHERE country <> 'Desconhecido'
        GROUP BY country ORDER BY titulos DESC LIMIT 10
    """).sort_values("titulos")
    ax = df.plot(kind="barh", x="pais", y="titulos", color=RED, legend=False, figsize=(8, 5))
    ax.set_title("Top 10 países por quantidade de títulos")
    ax.set_xlabel("Quantidade de títulos")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "02_top_paises.png", dpi=150)
    plt.close()


def chart_genre_trend(conn) -> None:
    df = query(conn, """
        SELECT g.genre, t.year_added AS ano, COUNT(*) AS titulos
        FROM titles t JOIN genres g ON g.show_id = t.show_id
        WHERE t.year_added IS NOT NULL
        GROUP BY g.genre, t.year_added
    """)
    top = df.groupby("genre")["titulos"].sum().nlargest(5).index
    pivot = df[df["genre"].isin(top)].pivot(index="ano", columns="genre", values="titulos").fillna(0)
    pivot = pivot[pivot.index >= pivot.index.max() - 8]
    ax = pivot.plot(marker="o", figsize=(10, 5))
    ax.set_title("Evolução dos 5 gêneros mais frequentes")
    ax.set_xlabel("Ano de entrada no catálogo")
    ax.set_ylabel("Quantidade de títulos")
    plt.tight_layout()
    plt.savefig(IMG_DIR / "03_tendencia_generos.png", dpi=150)
    plt.close()


def main() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        chart_additions_by_year(conn)
        chart_top_countries(conn)
        chart_genre_trend(conn)
    print(f"Gráficos salvos em {IMG_DIR}/")


if __name__ == "__main__":
    main()
