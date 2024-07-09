from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd
from datetime import datetime
import os


# função para pegar o codigo que será a chave primaria
def get_codigo(dataframe, nome_coluna, nome_coluna_nova):
    dataframe[nome_coluna_nova] = dataframe[nome_coluna].str[:9]
    return dataframe


# função para pegar o resto do identificar com apenas o nome
def get_nome(dataframe, nome_coluna, nome_coluna_nova):
    dataframe[nome_coluna_nova] = dataframe[nome_coluna].str[11:]
    return dataframe


# Função para converter strings formatadas com ponto e virgulas em float
def convert_to_float(value):
    return float(value.replace('.', '').replace(',', '.'))

# função para limpar os dados dos csvs brutos
def clean_data():
    # lendo os csvs e ja limpando colunas/linhas desnecessarias
    df_despesas = pd.read_csv(
        'gdvDespesasExcel.csv', encoding='latin-1')
    df_despesas.drop(columns=['Unnamed: 3'], inplace=True)
    df_despesas.drop(df_despesas.tail(1).index, inplace=True)
    df_despesas['Liquidado'] = df_despesas['Liquidado'].apply(convert_to_float)

    df_receita = pd.read_csv(
        'gdvReceitasExcel.csv', encoding='latin-1')
    df_receita.drop(columns=['Unnamed: 3'], inplace=True)
    df_receita.drop(df_receita.tail(1).index, inplace=True)
    df_receita['Arrecadado até 02/02/2024'] = df_receita['Arrecadado até 02/02/2024'].apply(
        convert_to_float)

    # extraindo codigo e nomes em colunas separadas
    df_despesas = get_codigo(df_despesas, 'Despesa', 'indice_despesas')
    df_receita = get_codigo(df_receita, 'Receita', 'indice_receita')
    df_despesas = get_nome(df_despesas, 'Despesa', 'nome_despesas')
    df_receita = get_nome(df_receita, 'Receita', 'nome_receita')

    # dropando colunas repetidas
    df_despesas.drop(columns=['Despesa'], inplace=True)
    df_receita.drop(columns=['Receita'], inplace=True)

    # ajeitando os valores para os tipos de dados correto
    df_despesas = df_despesas.astype({'Fonte de Recursos': 'string',
                                      'nome_despesas': 'string',
                                      'indice_despesas': 'int64',
                                      })
    df_receita = df_receita.astype({'Fonte de Recursos': 'string',
                                    'nome_receita': 'string',
                                    'indice_receita': 'int64',
                                    })

    # renomeando colunas para ficarem mais amigáveis pro banco de dados
    df_despesas.rename(columns={'Liquidado': 'valor_despesas',
                                'Fonte de Recursos': 'fonte_de_recursos'}, inplace=True)
    df_receita.rename(columns={'Arrecadado até 02/02/2024': 'valor_receita',
                               'Fonte de Recursos': 'fonte_de_recursos'}, inplace=True)

    # retornando os csvs para serem inseridos no aws s3
    df_despesas.to_csv('~/airflow/data/despesas.csv', sep=',', index=False, chunksize=1000)
    df_receita.to_csv('~/airflow/data/receita.csv', sep=',', index=False, chunksize=1000)


# função para fazer upload de uma pasta de csvs para o s3
def upload_csv_to_s3(**kwargs):
    bucket_name = 'curso-eng-vendas1234'
    local_folder_path = '/home/johnny/airflow/data'
    
    # conexão feita com variavel de ambiente (necessita configuração prévia no airflow)
    s3_hook = S3Hook(aws_conn_id='aws_s3_conn')

    # listando todos os arquivos csv
    for filename in os.listdir(local_folder_path):
        # fazendo o upload de cada arquivo no s3 na sua respectiva pasta
        if filename == 'receita.csv':
            local_file_path = os.path.join(local_folder_path, filename)
            s3_key = f'teste-esfera/receita/{filename}'
            
            s3_hook.load_file(
                filename=local_file_path,
                key=s3_key,
                bucket_name=bucket_name,
                replace=True
            )
        if filename == 'despesas.csv':
            local_file_path = os.path.join(local_folder_path, filename)
            s3_key = f'teste-esfera/despesas/{filename}'
            
            s3_hook.load_file(
                filename=local_file_path,
                key=s3_key,
                bucket_name=bucket_name,
                replace=True
            )

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 7),
    'retries': 1,
}


# DAGs 

with DAG('upload_multiple_csvs_to_s3_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    
    upload_task = PythonOperator(
        task_id='upload_csv_to_s3',
        python_callable=upload_csv_to_s3,
        provide_context=True
    )
    
    clean_data_task = PythonOperator(
        task_id='clean_data_task',
        python_callable=clean_data,
        provide_context=True
    )

clean_data_task >> upload_task
