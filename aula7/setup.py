import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# 1. Gerando o vendas.csv (Sem cabeçalho, índice na primeira coluna, 'ND' como nulo)
dados_csv = {
    'indice': [101, 102, 103, 104],
    'produto': ['Teclado', 'Mouse', 'Monitor', 'Gabinete'],
    'valor': [150.0, 'ND', 850.0, 'ND']
}
df_csv = pd.DataFrame(dados_csv).set_index('indice')
df_csv.to_csv('vendas.csv', header=False)
print("vendas.csv criado!")

# 2. Gerando o arquivo_existente.xlsx (Com a aba "Dados Brutos")
dados_excel = {
    'Data': ['2023-01-01', '2023-01-02'],
    'Vendas': [1500, 2300]
}
df_excel = pd.DataFrame(dados_excel)
df_excel.to_excel('arquivo_existente.xlsx', sheet_name='Dados Brutos', index=False)
print("arquivo_existente.xlsx criado!")

# 3. Gerando o banco de dados SQLite (meu_banco.db com a tabela "produtos")
engine = create_engine('sqlite:///meu_banco.db')
dados_sql = {
    'id': [1, 2, 3],
    'nome_produto': ['Mesa', 'Cadeira', 'Luminária'],
    'estoque': [15, 42, 10]
}
df_sql = pd.DataFrame(dados_sql)
df_sql.to_sql('produtos', con=engine, index=False, if_exists='replace')
print("Banco de dados SQLite meu_banco.db criado!")