import pandas as pd
import numpy as np
import mysql.connector
import json
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

def carregar_dados():
    with open('config.json', 'r') as file:
        configuracoes_db = json.load(file)

    cnx = mysql.connector.connect(**configuracoes_db)
    query = "SELECT * FROM economia_regional"
    df = pd.read_sql(query, cnx)
    cnx.close()
    return df

def preparar_dados(df):
    colunas_indices = [c for c in df.columns if c.startswith('indice_')]
    
    df_long = pd.melt(
        df, 
        id_vars=['data_referencia', 'valor_dolar'], 
        value_vars=colunas_indices, 
        var_name='estado', 
        value_name='indice_economico'
    )
    
    df_long['estado'] = df_long['estado'].str.replace('indice_', '').str.upper()
    df_long = df_long.dropna()

    def definir_perfil(uf):
        if uf in ['SP', 'RJ', 'MG']:
            return 'Industrial'
        elif uf in ['PR', 'RS', 'GO']:
            return 'Agro'
        else:
            return 'Servicos'
            
    df_long['classe_perfil'] = df_long['estado'].apply(definir_perfil)
    
    return df_long

def executar_knn():
    df_bruto = carregar_dados()
    df_ml = preparar_dados(df_bruto)

    X = df_ml[['valor_dolar', 'indice_economico']]
    y = df_ml['classe_perfil']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    valores_k = range(1, 16, 2)
    pesos = ['uniform', 'distance']
    
    melhor_acuracia = 0
    melhor_k = 0
    melhor_peso = ''
    resultados_cv = []

    print("\n--- INICIANDO VALIDAÇÃO CRUZADA (CV=5) ---")
    for k in valores_k:
        for w in pesos:
            knn = KNeighborsClassifier(n_neighbors=k, weights=w)
            scores = cross_val_score(knn, X_train_scaled, y_train, cv=5, scoring='accuracy')
            acuracia_media = scores.mean()
            
            resultados_cv.append((k, w, acuracia_media))
            print(f"K: {k:2d} | Peso: {w:8s} | Acurácia Média CV: {acuracia_media:.4f}")
            
            if acuracia_media > melhor_acuracia:
                melhor_acuracia = acuracia_media
                melhor_k = k
                melhor_peso = w

    print("\n--- MELHOR MODELO ENCONTRADO ---")
    print(f"Melhor K: {melhor_k}")
    print(f"Melhor Ponderação: {melhor_peso}")
    print(f"Acurácia na Validação (Treino): {melhor_acuracia:.4f}")

    modelo_final = KNeighborsClassifier(n_neighbors=melhor_k, weights=melhor_peso)
    modelo_final.fit(X_train_scaled, y_train)

    y_pred = modelo_final.predict(X_test_scaled)
    acuracia_teste = accuracy_score(y_test, y_pred)

    print("\n--- AVALIAÇÃO NO CONJUNTO DE TESTE (30% INÉDITOS) ---")
    print(f"Acurácia Final: {acuracia_teste:.4f}")
    print("\nRelatório de Classificação:")
    print(classification_report(y_test, y_pred))

    k_vals_uniform = [res[0] for res in resultados_cv if res[1] == 'uniform']
    acc_uniform = [res[2] for res in resultados_cv if res[1] == 'uniform']
    
    k_vals_distance = [res[0] for res in resultados_cv if res[1] == 'distance']
    acc_distance = [res[2] for res in resultados_cv if res[1] == 'distance']

    plt.figure(figsize=(10, 6))
    plt.plot(k_vals_uniform, acc_uniform, marker='o', label='Weights: Uniform', color='blue')
    plt.plot(k_vals_distance, acc_distance, marker='s', label='Weights: Distance', color='red', linestyle='dashed')
    plt.title('Desempenho do kNN na Validação Cruzada')
    plt.xlabel('Número de Vizinhos (K)')
    plt.ylabel('Acurácia Média (CV=5)')
    plt.xticks(valores_k)
    plt.legend()
    plt.grid(True)
    plt.savefig('grafico_knn_cv.png')
    print("\nGráfico de desempenho 'grafico_knn_cv.png' salvo com sucesso!")

if __name__ == "__main__":
    executar_knn()