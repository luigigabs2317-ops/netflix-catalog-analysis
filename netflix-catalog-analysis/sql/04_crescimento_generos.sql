-- Crescimento anual por gênero (LAG para variação ano a ano)
-- Obs.: o último ano do dataset costuma estar incompleto, interprete com cuidado.
WITH generos_relevantes AS (
    SELECT genre
    FROM genres
    GROUP BY genre
    HAVING COUNT(*) >= 100
),
por_ano AS (
    SELECT
        g.genre,
        t.year_added AS ano,
        COUNT(*) AS titulos
    FROM titles t
    JOIN genres g ON g.show_id = t.show_id
    WHERE g.genre IN (SELECT genre FROM generos_relevantes)
      AND t.year_added >= (SELECT MAX(year_added) - 5 FROM titles)
    GROUP BY g.genre, t.year_added
),
com_lag AS (
    SELECT
        genre,
        ano,
        titulos,
        LAG(titulos) OVER (PARTITION BY genre ORDER BY ano) AS titulos_ano_anterior
    FROM por_ano
)
SELECT
    genre AS genero,
    ano,
    titulos,
    titulos_ano_anterior,
    ROUND(100.0 * (titulos - titulos_ano_anterior) / titulos_ano_anterior, 1) AS variacao_pct
FROM com_lag
ORDER BY genero, ano;
