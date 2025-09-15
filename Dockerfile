# Comece com a imagem oficial do Airflow que já estamos usando
FROM apache/airflow:2.5.0

# Mude para o usuário padrão 'airflow' para seguir as boas práticas
USER airflow

# Instale os pacotes Python necessários para este usuário
# A flag --user garante que os pacotes sejam instalados no local correto
RUN pip install --no-cache-dir --user pandas apache-airflow-providers-postgres "SQLAlchemy<2.0" psycopg2-binary dbt-core dbt-postgres