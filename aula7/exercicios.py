import pandas as pd
import requests
from sqlalchemy import create_engine

df_vendas = pd.read_csv('vendas.csv', header=None, index_col=0, na_values=['ND'])
print("--- Dados do CSV ---")
print(df_vendas)
print("\n")

relatorio_anual = pd.DataFrame()
relatorio_anual.to_excel('relatorio.xlsx', sheet_name='Resultados')

df_dados_brutos = pd.read_excel('arquivo_existente.xlsx', sheet_name='Dados Brutos')
print("--- Dados do Excel Existente ---")
print(df_dados_brutos)
print("\n")

resposta = requests.get('https://jsonplaceholder.typicode.com/users')
df_usuarios = pd.DataFrame(resposta.json())
print("--- Dados da API Web (5 primeiros) ---")
print(df_usuarios.head()) 
print("\n")

engine = create_engine('sqlite:///meu_banco.db')
df_produtos = pd.read_sql_table('produtos', con=engine)
print("--- Dados do Banco SQLite ---")
print(df_produtos)
print("\n")