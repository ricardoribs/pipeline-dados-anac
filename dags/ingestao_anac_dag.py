from __future__ import annotations

import pandas as pd
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

def ingest_data():
    """
    Função para ler dados de um CSV na pasta 'data' e ingeri-los
    em uma tabela 'voos_brutos' no banco de dados Postgres.
    A tabela será substituída se já existir.
    """
    # Conecta-se ao Postgres usando a connection_id 'postgres_anac'
    # que configuramos na interface do Airflow.
    hook = PostgresHook(postgres_conn_id='postgres_anac')
    engine = hook.get_sqlalchemy_engine()
    
    # Caminho para o arquivo CSV dentro do contêiner do Airflow
    csv_filepath = '/opt/airflow/data/Anexo I.csv'
    
    # Lê o CSV usando pandas
    df = pd.read_csv(csv_filepath, delimiter=';', encoding='latin1', skiprows=1)

    # Limpa os nomes das colunas para serem compatíveis com SQL
    df.columns = [c.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_') for c in df.columns]
    
    # Envia os dados para o Postgres, substituindo a tabela se ela já existir.
    df.to_sql('voos_brutos', engine, if_exists='replace', index=False)
    print(f"Dados do arquivo {csv_filepath} ingeridos com sucesso na tabela voos_brutos.")


with DAG(
    dag_id='ingestao_dados_anac',
    start_date=datetime(2025, 1, 1),
    schedule=None,  # A DAG não vai rodar automaticamente, apenas quando disparada manualmente.
    catchup=False,
    tags=['anac', 'postgres'],
) as dag:
    ingest_task = PythonOperator(
        task_id='ingest_anac_data_to_postgres',
        python_callable=ingest_data,
    )