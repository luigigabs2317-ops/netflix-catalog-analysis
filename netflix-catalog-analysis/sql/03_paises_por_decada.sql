-- Top 5 países por década de lançamento (RANK com window function)
WITH base AS (
    SELECT
        c.country,
        t.decade,
        COUNT(DISTINCT t.show_id) AS titulos
    FROM titles t
    JOIN countries c ON c.show_id = t.show_id
    WHERE c.country <> 'Desconhecido'
      AND t.decade >= 1980
    GROUP BY c.country, t.decade
),
ranked AS (
    SELECT
        *,
        RANK() OVER (PARTITION BY decade ORDER BY titulos DESC) AS posicao
    FROM base
)
SELECT decade AS decada, posicao, country AS pais, titulos
FROM ranked
WHERE posicao <= 5
ORDER BY decada, posicao;
