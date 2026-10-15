-- Top 10 países com mais títulos (um título com vários países conta para cada um)
SELECT
    country AS pais,
    COUNT(DISTINCT show_id) AS titulos,
    ROUND(100.0 * COUNT(DISTINCT show_id) / (SELECT COUNT(*) FROM titles), 1) AS pct_do_catalogo
FROM countries
WHERE country <> 'Desconhecido'
GROUP BY country
ORDER BY titulos DESC
LIMIT 10;
