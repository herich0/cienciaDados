import requests
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta

IBCR_SERIES = {
    'SP': 25392, 'RJ': 25396, 'MG': 25379, 'RS': 25401, 'CE': 25390,
    'BA': 25386, 'PE': 25399, 'PR': 25400, 'SC': 25414, 'GO': 25388,
    'PA': 25409, 'AM': 25382, 'ES': 25387
}

def executar_pipeline():
    try:
        hoje = datetime.now()
        data_final = hoje.strftime('%d/%m/%Y')
        data_inicial = (hoje - timedelta(days=3650)).strftime('%d/%m/%Y')
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        
        print("Extraindo dados do Dólar (BCB)...", end=" ", flush=True)
        url_dolar = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
        resp_dolar = requests.get(url_dolar, headers=headers)
        resp_dolar.raise_for_status()
        
        try:
            dados_dolar = resp_dolar.json()
        except ValueError:
            print("ERRO: A API do Dólar retornou vazio.")
            return

        print("OK!")

        df_dolar = pd.DataFrame(dados_dolar)
        df_dolar['data'] = pd.to_datetime(df_dolar['data'], format='%d/%m/%Y')
        df_dolar['valor_dolar'] = pd.to_numeric(df_dolar['valor'])
        df_dolar = df_dolar.drop(columns=['valor'])
        
        df_completo = df_dolar.copy()
        
        print("Extraindo IBCR de 13 Estados (BCB)...")
        for estado, codigo in IBCR_SERIES.items():
            print(f"  - Baixando {estado}... ", end="", flush=True)
            url_ibcr = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"
            resp = requests.get(url_ibcr, headers=headers)
            
            if resp.status_code == 200:
                try:
                    dados_ibcr = resp.json()
                    df_ibcr = pd.DataFrame(dados_ibcr)
                    if not df_ibcr.empty:
                        df_ibcr['data'] = pd.to_datetime(df_ibcr['data'], format='%d/%m/%Y')
                        df_ibcr[f'indice_{estado.lower()}'] = pd.to_numeric(df_ibcr['valor'])
                        df_ibcr = df_ibcr.drop(columns=['valor'])
                        df_completo = pd.merge(df_completo, df_ibcr, on='data', how='left')
                        print("OK!")
                    else:
                        print("Vazio!")
                except ValueError:
                    print("Erro no JSON. Pulando...")
                    continue
            else:
                print(f"Erro {resp.status_code}")
        
        df_completo = df_completo.ffill().dropna()

        try:
            with open('config.json', 'r') as file:
                configuracoes_db = json.load(file)
        except Exception as err:
            print(f"Erro Crítico ao ler config.json: {err}")
            return

        try:
            cnx = mysql.connector.connect(**configuracoes_db)
        except mysql.connector.Error as err:
            print(f"Erro ao conectar no banco: {err}")
            return 
            
        print(f"Conexão ativa no banco: {cnx.database}")
            
        cursor = cnx.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS economia_regional")
        
        lista_ufs = list(IBCR_SERIES.keys())
        colunas_ddl = ", ".join([f"indice_{uf.lower()} DECIMAL(10,2)" for uf in lista_ufs])
        
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS economia_regional (
                data_referencia DATE PRIMARY KEY,
                valor_dolar DECIMAL(10,4),
                {colunas_ddl}
            )
        """)
        
        colunas_insert = ", ".join([f"indice_{uf.lower()}" for uf in lista_ufs])
        placeholders = ", ".join(["%s"] * (2 + len(lista_ufs)))
        updates = ", ".join([f"indice_{uf.lower()} = VALUES(indice_{uf.lower()})" for uf in lista_ufs])
        
        query_insert = f"""
            INSERT INTO economia_regional (data_referencia, valor_dolar, {colunas_insert})
            VALUES ({placeholders})
            ON DUPLICATE KEY UPDATE 
                valor_dolar = VALUES(valor_dolar),
                {updates}
        """
        
        tuplas_dados = []
        for _, row in df_completo.iterrows():
            linha_tupla = [row['data'].strftime('%Y-%m-%d'), row['valor_dolar']]
            for uf in lista_ufs:
                col_name = f"indice_{uf.lower()}"
                linha_tupla.append(row.get(col_name, None))
            tuplas_dados.append(tuple(linha_tupla))
            
        if not cnx.in_transaction:
            cursor.executemany(query_insert, tuplas_dados)
            cnx.commit()
            print(f"Processamento de {cursor.rowcount} linhas (13 UFs) concluído no banco.")

        cursor.execute('SELECT data_referencia, valor_dolar, indice_sp, indice_pr, indice_pe FROM economia_regional ORDER BY data_referencia ASC')
        dados_db = cursor.fetchall()
            
        df_db = pd.DataFrame(dados_db, columns=['Data', 'Dolar', 'SP', 'PR', 'PE'])
        df_db['Data'] = pd.to_datetime(df_db['Data'])
        for col in ['Dolar', 'SP', 'PR', 'PE']:
            df_db[col] = pd.to_numeric(df_db[col])
            
        fig = plt.figure(figsize=(16, 10))
        
        plt.subplot(2, 2, 1)
        plt.plot(df_db['Data'], df_db['Dolar'], color='green', linewidth=1.5)
        plt.title('Evolução Diária do Dólar')
        plt.grid(True)
        
        plt.subplot(2, 2, 2)
        plt.plot(df_db['Data'], df_db['SP'], label='São Paulo', color='blue')
        plt.plot(df_db['Data'], df_db['PR'], label='Paraná', color='orange')
        plt.plot(df_db['Data'], df_db['PE'], label='Pernambuco', color='purple')
        plt.title('Comparativo Regional (IBCR - Banco Central)')
        plt.legend()
        plt.grid(True)

        plt.subplot(2, 1, 2)
        plt.scatter(df_db['Dolar'], df_db['SP'], alpha=0.5, color='blue', label='SP')
        plt.scatter(df_db['Dolar'], df_db['PR'], alpha=0.5, color='orange', label='PR')
        plt.title('Dispersão: Dólar vs Atividade (Preparação para kNN)')
        plt.xlabel('Valor do Dólar (R$)')
        plt.ylabel('Índice IBCR')
        plt.legend()
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('graficos_brasil_13ufs.png')
        print("Gráficos salvos com sucesso na pasta atual!")
        
        cursor.close()
        demonstrar_comandos_internos(cnx)
        cnx.disconnect() 
        
    except Exception as e:
        print(f"Erro crítico: {str(e)}")

def demonstrar_comandos_internos(cnx):
    try:
        if hasattr(cnx, 'get_database'):
            cnx.get_database()
        cnx.cmd_init_db('teste')
        cnx.set_database('teste')
        cnx.cmd_query("SELECT 1")
        cnx.cmd_quit()
    except Exception as err:
        pass

if __name__ == "__main__":
    executar_pipeline()