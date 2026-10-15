-- Distribuição de classificação indicativa nos 5 países com mais títulos
WITH top_paises AS (
    SELECT country
    FROM countries
    WHERE country <> 'Desconhecido'
    GROUP BY country
    ORDER BY COUNT(DISTINCT show_id) DESC
    LIMIT 5
),
distribuicao AS (
    SELECT
        c.country,
        t.rating,
        COUNT(DISTINCT t.show_id) AS titulos
    FROM titles t
    JOIN countries c ON c.show_id = t.show_id
    WHERE c.country IN (SELECT country FROM top_paises)
    GROUP BY c.country, t.rating
)
SELECT
    country AS pais,
    rating AS classificacao,
    titulos,
    ROUND(100.0 * titulos / SUM(titulos) OVER (PARTITION BY country), 1) AS pct_no_pais
FROM distribuicao
ORDER BY pais, titulos DESC;
