# Análise de Catálogo e Tendências da Netflix

![Testes](https://github.com/luigigabs2317-ops/netflix-catalog-analysis/actions/workflows/tests.yml/badge.svg)

Projeto de análise de dados que explora o catálogo da Netflix (filmes e séries) para identificar tendências de conteúdo e a distribuição por país. O fluxo completo cobre **tratamento com Python**, **análise com SQL** e **dashboard no Power BI com DAX**.

**Nível:** iniciante a intermediário

## Perguntas de negócio

- A proporção de séries em relação a filmes mudou ao longo dos anos?
- Quais países mais produzem conteúdo no catálogo e como isso mudou por década?
- Quais gêneros mais cresceram nos últimos anos?
- Quanto tempo, em média, um título leva entre o lançamento original e a entrada na plataforma?
- Como a classificação indicativa se distribui entre os principais países?

## Tecnologias

| Etapa | Ferramentas |
|-------|-------------|
| Tratamento de dados | Python 3.10+, pandas |
| Análise | SQL (SQLite): CTEs, `JOIN`, `RANK()`, `LAG()` |
| Visualização | Power BI (modelo estrela + DAX), matplotlib |
| Qualidade | pytest, GitHub Actions |

## Estrutura do repositório

```
netflix-catalog-analysis/
├── data/
│   ├── raw/             # CSV original do Kaggle (não versionado)
│   └── processed/       # titles.csv, genres.csv, countries.csv
├── src/
│   ├── clean_data.py    # limpeza e criação de colunas derivadas
│   ├── load_to_sqlite.py
│   ├── run_queries.py   # executa sql/*.sql e salva em outputs/
│   └── charts.py        # gráficos para o README
├── sql/                 # 7 consultas analíticas
├── outputs/             # resultados das consultas em CSV
├── powerbi/             # medidas DAX e guia de montagem do dashboard
├── tests/               # testes da etapa de limpeza
└── docs/img/            # gráficos e prints do dashboard
```

## Como executar

```bash
git clone https://github.com/luigigabs2317-ops/netflix-catalog-analysis.git
cd netflix-catalog-analysis
pip install -r requirements.txt

# 1. Baixe netflix_titles.csv (ver data/raw/README.md) e coloque em data/raw/
python src/clean_data.py       # gera data/processed/*.csv
python src/load_to_sqlite.py   # cria data/netflix.db
python src/run_queries.py      # executa as consultas SQL
python src/charts.py           # gera os gráficos em docs/img/

pytest                         # roda os testes
```

## Tratamento dos dados

Principais problemas resolvidos em `clean_data.py`:

- Datas em texto (`September 25, 2021`) convertidas para data, com espaços extras removidos.
- Algumas linhas trazem a duração (ex.: `74 min`) na coluna de classificação; os valores são movidos para o campo correto.
- Duração separada em valor e unidade (minutos para filmes, temporadas para séries).
- Valores ausentes em país, diretor e classificação tratados como categorias explícitas.
- Colunas com múltiplos valores (`country`, `listed_in`) transformadas em tabelas N:N (`countries`, `genres`).
- Colunas derivadas: `year_added`, `month_added`, `decade` e `release_gap` (anos entre o lançamento e a entrada no catálogo).

## Modelo de dados

```
titles (fato)  1 ──── N  genres     (show_id, genre)
               1 ──── N  countries  (show_id, country)
               N ──── 1  Calendario (date_added)
```

## Consultas SQL

| Arquivo | Pergunta |
|---------|----------|
| `01_filmes_vs_series_por_ano.sql` | Proporção de filmes e séries por ano de entrada |
| `02_top_paises.sql` | Top 10 países com mais títulos |
| `03_paises_por_decada.sql` | Top 5 países por década (`RANK`) |
| `04_crescimento_generos.sql` | Variação anual por gênero (`LAG`) |
| `05_intervalo_lancamento_adicao.sql` | Intervalo médio entre lançamento e entrada no catálogo |
| `06_classificacao_por_pais.sql` | Classificação indicativa nos principais países |
| `07_duracao_media.sql` | Duração média de filmes e temporadas de séries por década |

## Dashboard Power BI

As medidas DAX estão em [`powerbi/medidas.dax`](powerbi/medidas.dax) e o passo a passo de montagem em [`powerbi/README.md`](powerbi/README.md).

<!-- Adicione aqui os prints do dashboard, por exemplo:
![Visão geral](docs/img/dashboard_visao_geral.png)
-->

## Gráficos

![Adições por ano](docs/img/01_adicoes_por_ano.png)
![Top países](docs/img/02_top_paises.png)
![Tendência de gêneros](docs/img/03_tendencia_generos.png)

## Principais insights

<!-- Preencha com 3 a 5 conclusões baseadas nos resultados reais de outputs/ e do dashboard. -->

## Limitações

- O dataset é um recorte público do catálogo (até 2021) e não representa o catálogo atual nem varia por região.
- Títulos com mais de um país contam uma vez para cada país.
- O último ano do dataset está incompleto, então comparações anuais dele devem ser feitas com cautela.

## Fonte dos dados

[Netflix Movies and TV Shows (Kaggle)](https://www.kaggle.com/datasets/shivamb/netflix-shows)

## Autor

Luigi Gabriel Ferreira Dias — [GitHub](https://github.com/luigigabs2317-ops)
