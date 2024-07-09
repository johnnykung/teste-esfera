from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd

# DAG
dag = DAG('eda', description='DAG de EDA para análise e limpeza dos dados',
          schedule_interval=None, start_date=datetime(2024,7,7),
          catchup=False)

# funções

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


def main():
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



task_eda = PythonOperator(task_id='task_eda', python_callable=main, dag=dag)

task_eda