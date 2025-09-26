# ETL de Filmes Populares

Este projeto é um pipeline de ETL (Extração, Transformação e Carga) que coleta dados sobre filmes populares de múltiplas fontes, os consolida e armazena em um banco de dados SQLite.

## Tecnologias Utilizadas (Stacks)

| Tecnologia/Stack | Utilização no Projeto |
| :--- | :--- |
| **Pandas** | Usado para estruturar, manipular e limpar os dados coletados. Todas as informações da API e do web scraping são organizadas em um `DataFrame` antes de serem salvas. |
| **Requests** | Responsável por realizar as requisições HTTP para a API do TMDB e para buscar o conteúdo HTML bruto das páginas do IMDb antes do parsing. |
| **Beautiful Soup** | Utilizado para fazer o parsing do HTML estático obtido das páginas do IMDb, permitindo a extração fácil de informações como a nota e o nome do diretor. |
| **Selenium** | Essencial para o web scraping dinâmico no site Rotten Tomatoes. Ele automatiza um navegador para interagir com a página e extrair a pontuação da crítica, que é carregada via JavaScript e não seria acessível apenas com `Requests`. |
| **Apache Airflow** | Atua como o orquestrador do pipeline. É usado para agendar, monitorar e executar as tarefas de ETL (transform e load) de forma automatizada e em uma sequência definida (DAG). |

## O que o projeto faz?

O pipeline executa as seguintes etapas:

1.  **Extração (Extract)**:
    * Busca uma lista de filmes populares da API do **The Movie Database (TMDB)**.
    * Para cada filme, realiza web scraping em duas fontes para obter dados adicionais:
        * **IMDb**: Coleta a nota dos usuários e o nome do diretor.
        * **Rotten Tomatoes**: Coleta a pontuação da crítica (Tomatometer) usando Selenium para lidar com conteúdo dinâmico.

2.  **Transformação (Transform)**:
    * Os dados coletados de todas as fontes são combinados e estruturados em um DataFrame do Pandas.
    * As colunas são selecionadas e reordenadas para criar um conjunto de dados limpo e coeso.

3.  **Carga (Load)**:
    * O DataFrame final é carregado em uma tabela chamada `movies` dentro de um banco de dados SQLite (`movies.db`), substituindo os dados antigos a cada nova execução.

O projeto foi projetado para ser executado tanto localmente para testes rápidos quanto orquestrado com **Apache Airflow** para execuções agendadas e automatizadas.

***

## ⚙️ Como Rodar o Projeto

Você pode executar este pipeline de duas maneiras: localmente em sua máquina ou usando o Airflow com Docker.

### 1. Rodando Localmente

Esta abordagem é ideal para testes e desenvolvimento.

#### Pré-requisitos
* Python 3.11+
* Git
* Google Chrome
* [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) compatível com a sua versão do Chrome.
    * **Observação**: O caminho para o `chromedriver` está definido como `/usr/local/bin/chromedriver` no arquivo `etl/extract_web_rttm.py`. Se o seu executável estiver em outro local, você precisará atualizar este caminho.

#### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/gusrberto/etl-popular-movies.git
    cd etl-popular-movies
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    * Copie o arquivo de exemplo:
        ```bash
        cp .env.example .env
        ```
    * Abra o arquivo `.env` e preencha as variáveis:
        * `TMDB_API_KEY`: Sua chave de API do [The Movie Database](https://www.themoviedb.org/documentation/api).
        * `NUMBER_OF_MOVIES_TO_SCRAP`: O número de filmes que você deseja processar (ex: `25`).

5.  **Execute o pipeline:**
    ```bash
    python test_local_pipeline.py
    ```
    Ao final da execução, o banco de dados `local_data/movies.db` será criado ou atualizado com os dados mais recentes.

***

### 2. Rodando com Airflow (via Docker)

Esta abordagem usa Docker e Docker Compose para orquestrar o pipeline com o Apache Airflow, ideal para produção e agendamentos.

#### Pré-requisitos
* Docker
* Docker Compose

#### Passos

1.  **Configure as variáveis de ambiente:**
    * Copie o arquivo de exemplo (se ainda não tiver feito no passo anterior):
        ```bash
        cp .env.example .env
        ```
    * Abra o arquivo `.env` e preencha **todas** as variáveis:
        * `TMDB_API_KEY`: Sua chave de API do TMDB.
        * `NUMBER_OF_MOVIES_TO_SCRAP`: Número de filmes a processar.
        * `UID` e `GID`: Seu User ID e Group ID. Eles são necessários para evitar problemas de permissão de arquivos gerados pelo Airflow. Para obtê-los, execute os seguintes comandos no seu terminal:
            ```bash
            echo "UID=$(id -u)" >> .env
            echo "GID=$(id -g)" >> .env
            ```

2.  **Construa e inicie os containers do Airflow:**
    ```bash
    docker compose up --build
    ```
    *Use a flag `-d` para rodar em modo detached (em segundo plano).*

3.  **Acesse a interface do Airflow:**
    * Abra seu navegador e acesse `http://localhost:8080`.
    * Usuário: `admin`.
    * Senha: o Airflow Standalone gera uma nova senha aleatória a cada build, por isso após subir o contâiner, identifique a senha que foi gerada.

4.  **Ative e execute a DAG:**
    * Na lista de DAGs, encontre `etl_movies_dag`.
    * Ative o toggle no lado esquerdo para habilitar a DAG.
    * Para executá-la manualmente, clique no botão "Play" (▶️) na coluna de ações.

Após a execução, os dados serão salvos no arquivo `data/movies.db` dentro do volume do Docker, que está mapeado para o diretório `data` no seu host local.