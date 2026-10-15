-- Intervalo médio (em anos) entre o lançamento original e a entrada no catálogo
SELECT
    year_added AS ano,
    type AS tipo,
    COUNT(*) AS titulos,
    ROUND(AVG(release_gap), 1) AS intervalo_medio_anos
FROM titles
WHERE release_gap IS NOT NULL
  AND release_gap >= 0
GROUP BY year_added, type
ORDER BY year_added, type;
