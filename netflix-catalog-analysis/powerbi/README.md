# Dashboard Power BI

## Como montar

1. **Obter dados > Texto/CSV**: importe `data/processed/titles.csv`, `genres.csv` e `countries.csv`.
2. No Power Query, confira os tipos: `date_added` como **Data**, `release_year`, `year_added`, `decade` como **Número inteiro**.
3. Crie a tabela `Calendario` e as medidas de `medidas.dax`.
4. Monte o modelo (aba **Modelo**):

| De | Para | Cardinalidade | Direção do filtro |
|----|------|---------------|-------------------|
| `titles[show_id]` | `genres[show_id]` | 1:N | **Ambas** |
| `titles[show_id]` | `countries[show_id]` | 1:N | **Ambas** |
| `Calendario[Date]` | `titles[date_added]` | 1:N | Única |

> `genres` e `countries` são tabelas de relação N:N (um título tem vários gêneros e países).
> A direção **Ambas** é necessária para que um filtro de gênero ou país reduza os títulos.

## Páginas sugeridas

1. **Visão geral**: cartões (Total Títulos, % Filmes, % Séries, Total Países), colunas empilhadas de adições por ano e tipo, segmentação por tipo.
2. **Gêneros**: barras com ranking de gêneros, linha com evolução ao longo dos anos, segmentação por tipo e período.
3. **Geografia**: mapa de bolhas por país, barras com Top 10 e `% do Catálogo`, segmentação por ano e tipo.

## Observações

- Títulos sem `date_added` não aparecem nas análises temporais baseadas no calendário.
- O último ano do dataset está incompleto, então o `Crescimento YoY` dele não é comparável.
- Salve o arquivo como `powerbi/netflix_dashboard.pbix` e coloque prints em `docs/img/`.
