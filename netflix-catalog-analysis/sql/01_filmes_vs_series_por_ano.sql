-- Proporção de filmes vs. séries por ano de entrada no catálogo
SELECT
    year_added AS ano,
    SUM(CASE WHEN type = 'Movie'   THEN 1 ELSE 0 END) AS filmes,
    SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) AS series,
    COUNT(*) AS total,
    ROUND(100.0 * SUM(CASE WHEN type = 'TV Show' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_series
FROM titles
WHERE year_added IS NOT NULL
GROUP BY year_added
ORDER BY year_added;
