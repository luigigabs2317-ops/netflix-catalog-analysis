-- Duração média de filmes (minutos) e de séries (temporadas) por década de lançamento
SELECT
    decade AS decada,
    type AS tipo,
    duration_unit AS unidade,
    COUNT(*) AS titulos,
    ROUND(AVG(duration_value), 1) AS duracao_media
FROM titles
WHERE duration_value IS NOT NULL
  AND decade >= 1980
GROUP BY decade, type, duration_unit
ORDER BY decada, tipo;
