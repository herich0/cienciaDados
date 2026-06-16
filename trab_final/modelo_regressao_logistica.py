import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def carregar_dados():
    with open('config.json', 'r') as file:
        configuracoes_db = json.load(file)

    cnx = mysql.connector.connect(**configuracoes_db)
    query = "SELECT valor_dolar, indice_sp, indice_mg FROM economia_regional"
    df = pd.read_sql(query, cnx)
    cnx.close()
    return df.dropna()

def executar_regressao_logistica():
    df = carregar_dados()

    mediana_sp = df['indice_sp'].median()
    df['sp_aquecido'] = (df['indice_sp'] > mediana_sp).astype(int)

    X = df[['valor_dolar', 'indice_mg']]
    y = df['sp_aquecido']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    modelo = LogisticRegression(solver='sag', random_state=42, max_iter=1000)
    modelo.fit(X_train_scaled, y_train)

    y_pred = modelo.predict(X_test_scaled)

    print("--- MÉTRICAS DE DESEMPENHO (CONJUNTO DE TESTE) ---")
    print(f"Acurácia: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precisão: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:   {recall_score(y_test, y_pred):.4f}")
    print(f"F1-Score: {f1_score(y_test, y_pred):.4f}")

    print("\n--- INTERPRETAÇÃO DOS COEFICIENTES ---")
    print(f"Coeficiente Dólar (Beta 1): {modelo.coef_[0][0]:.4f}")
    print(f"Coeficiente MG    (Beta 2): {modelo.coef_[0][1]:.4f}")

    x_min, x_max = X_test_scaled[:, 0].min() - 0.5, X_test_scaled[:, 0].max() + 0.5
    y_min, y_max = X_test_scaled[:, 1].min() - 0.5, X_test_scaled[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))

    Z = modelo.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.figure(figsize=(10, 6))
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
    
    scatter = plt.scatter(X_test_scaled[:, 0], X_test_scaled[:, 1], c=y_test, edgecolor='k', cmap='coolwarm')
    
    plt.title('Fronteira de Decisão: Regressão Logística')
    plt.xlabel('Valor do Dólar (Padronizado)')
    plt.ylabel('Índice de MG (Padronizado)')
    
    handles, labels = scatter.legend_elements()
    plt.legend(handles, ['Desaquecido (0)', 'Aquecido (1)'])
    
    plt.tight_layout()
    plt.savefig('grafico_regressao_logistica.png')
    print("\nGráfico 'grafico_regressao_logistica.png' salvo com sucesso na pasta atual!")

if __name__ == "__main__":
    executar_regressao_logistica()