import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from clean_data import clean_titles, explode_column  # noqa: E402


def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "show_id": ["s1", "s2", "s3"],
            "type": ["Movie", "TV Show", "Movie"],
            "title": ["A", "B", "C"],
            "director": [None, "Fulano", "Ciclano"],
            "cast": [None, None, None],
            "country": ["United States, India", None, "Brazil"],
            "date_added": [" September 25, 2021", "January 1, 2019", None],
            "release_year": [2020, 2017, 2010],
            "rating": ["PG-13", "TV-MA", "74 min"],
            "duration": ["90 min", "2 Seasons", None],
            "listed_in": ["Dramas, Comedies", "Docuseries", "Comedies"],
            "description": ["", "", ""],
        }
    )


def test_duration_moved_from_rating():
    out = clean_titles(sample_df()).set_index("show_id")
    assert out.loc["s3", "duration_value"] == 74
    assert out.loc["s3", "duration_unit"] == "min"
    assert out.loc["s3", "rating"] == "Não informado"


def test_dates_and_derived_columns():
    out = clean_titles(sample_df()).set_index("show_id")
    assert out.loc["s1", "year_added"] == 2021
    assert out.loc["s1", "release_gap"] == 1
    assert pd.isna(out.loc["s3", "year_added"])
    assert out.loc["s2", "decade"] == 2010


def test_missing_values_become_categories():
    out = clean_titles(sample_df()).set_index("show_id")
    assert out.loc["s2", "country"] == "Desconhecido"
    assert out.loc["s1", "director"] == "Não informado"


def test_seasons_normalized():
    out = clean_titles(sample_df()).set_index("show_id")
    assert out.loc["s2", "duration_unit"] == "season"
    assert out.loc["s2", "duration_value"] == 2


def test_explode_column_splits_and_strips():
    df = sample_df()
    out = explode_column(df, "listed_in", "genre")
    assert len(out) == 4
    assert set(out[out["show_id"] == "s1"]["genre"]) == {"Dramas", "Comedies"}
