# ETL Popular Movies

Este projeto é um pipeline ETL em Python que coleta dados de filmes populares, faz enriquecimento com notas e diretores de sites externos, e armazena os resultados em um banco de dados SQLite. O pipeline pode ser executado localmente ou utilizando Apache Airflow em Docker.

## Estrutura do Projeto

.
├── dags                    # DAG do Airflow
│   └── popular_movies_dag.py
├── data                    # Banco SQLite (movies.db)
├── docker-compose.yaml     # Configuração do Docker Compose
├── Dockerfile              # Imagem do Airflow
├── .env                    # Variáveis de ambiente
├── .env.example            # Exemplo de variáveis de ambiente
├── etl                     # Scripts ETL
│   ├── extract_api.py
│   ├── extract_web_imdb.py
│   ├── extract_web_rttm.py
│   ├── load.py
│   └── transform.py
├── requirements.txt
├── test_local_pipeline.py  # Script para execução local do ETL
└── README.md
