"""Limpeza e preparação do dataset Netflix Movies and TV Shows.

Entrada : data/raw/netflix_titles.csv
Saída   : data/processed/titles.csv, genres.csv, countries.csv

Uso:
    python src/clean_data.py
"""
from pathlib import Path

import pandas as pd

RAW_PATH = Path("data/raw/netflix_titles.csv")
OUT_DIR = Path("data/processed")


def clean_titles(df: pd.DataFrame) -> pd.DataFrame:
    """Retorna a tabela principal de títulos, limpa e com colunas derivadas."""
    df = df.copy()

    # Remove espaços em branco sobrando em todas as colunas de texto
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()

    # Algumas linhas trazem a duração (ex.: "74 min") na coluna rating
    misplaced = df["rating"].fillna("").str.contains("min", case=False)
    df.loc[misplaced, "duration"] = df.loc[misplaced, "rating"]
    df.loc[misplaced, "rating"] = pd.NA

    df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"] = df["date_added"].dt.year.astype("Int64")
    df["month_added"] = df["date_added"].dt.month.astype("Int64")

    # Anos entre o lançamento original e a entrada no catálogo
    df["release_gap"] = df["year_added"] - df["release_year"]
    df["decade"] = (df["release_year"] // 10 * 10).astype(int)

    # Duração: minutos para filmes, temporadas para séries
    df["duration_value"] = pd.to_numeric(
        df["duration"].str.extract(r"(\d+)")[0], errors="coerce"
    )
    df["duration_unit"] = (
        df["duration"].str.extract(r"([A-Za-z]+)")[0].str.lower().str.replace("seasons", "season")
    )

    # Valores ausentes viram categorias explícitas
    df["country"] = df["country"].fillna("Desconhecido")
    df["director"] = df["director"].fillna("Não informado")
    df["rating"] = df["rating"].fillna("Não informado")

    df = df.drop_duplicates(subset="show_id")

    columns = [
        "show_id", "type", "title", "director", "country", "date_added",
        "year_added", "month_added", "release_year", "decade", "release_gap",
        "rating", "duration_value", "duration_unit",
    ]
    return df[columns]


def explode_column(df: pd.DataFrame, source: str, target: str) -> pd.DataFrame:
    """Transforma uma coluna com valores separados por vírgula em tabela N:N."""
    out = df[["show_id", source]].copy()
    out[target] = out[source].str.split(",")
    out = out.explode(target)
    out[target] = out[target].str.strip()
    out = out[out[target].notna() & (out[target] != "")]
    return out[["show_id", target]].drop_duplicates()


def main() -> None:
    if not RAW_PATH.exists():
        raise SystemExit(f"Arquivo não encontrado: {RAW_PATH}. Veja data/raw/README.md")

    raw = pd.read_csv(RAW_PATH)
    print(f"Linhas lidas: {len(raw)}")

    titles = clean_titles(raw)
    genres = explode_column(raw.assign(listed_in=raw["listed_in"].fillna("Desconhecido")),
                            "listed_in", "genre")
    countries = explode_column(raw.assign(country=raw["country"].fillna("Desconhecido")),
                               "country", "country")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    titles.to_csv(OUT_DIR / "titles.csv", index=False)
    genres.to_csv(OUT_DIR / "genres.csv", index=False)
    countries.to_csv(OUT_DIR / "countries.csv", index=False)

    print(f"titles.csv   : {len(titles)} linhas")
    print(f"genres.csv   : {len(genres)} linhas")
    print(f"countries.csv: {len(countries)} linhas")
    print(f"Títulos sem date_added: {titles['date_added'].isna().sum()}")


if __name__ == "__main__":
    main()
