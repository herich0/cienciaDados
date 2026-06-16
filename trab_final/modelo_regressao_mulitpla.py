import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mysql.connector
import statsmodels.api as sm
from sklearn.linear_model import Ridge, Lasso
from sklearn.preprocessing import StandardScaler

def carregar_dados():
    with open('config.json', 'r') as file:
        configuracoes_db = json.load(file)
    cnx = mysql.connector.connect(**configuracoes_db)
    query = "SELECT valor_dolar, indice_sp, indice_mg, indice_pr FROM economia_regional"
    df = pd.read_sql(query, cnx)
    cnx.close()
    return df.dropna()

def executar_regressao_multipla():
    df = carregar_dados()
    
    df['dolar_quadrado'] = df['valor_dolar'] ** 2
    
    y = df['indice_sp']
    X = df[['valor_dolar', 'indice_mg', 'indice_pr', 'dolar_quadrado']]
    
    X_sm = sm.add_constant(X)
    modelo_ols = sm.OLS(y, X_sm).fit()
    
    print(modelo_ols.summary())
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    alphas = np.logspace(-3, 4, 100)
    coefs_ridge = []
    coefs_lasso = []
    
    for a in alphas:
        ridge = Ridge(alpha=a)
        ridge.fit(X_scaled, y)
        coefs_ridge.append(ridge.coef_)
        
        lasso = Lasso(alpha=a, max_iter=10000)
        lasso.fit(X_scaled, y)
        coefs_lasso.append(lasso.coef_)
        
    plt.figure(figsize=(14, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(alphas, coefs_ridge)
    plt.xscale('log')
    plt.title('Ridge Regression: Coeficientes vs Alpha')
    plt.xlabel('Alpha')
    plt.ylabel('Coeficientes')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(alphas, coefs_lasso)
    plt.xscale('log')
    plt.title('Lasso Regression: Coeficientes vs Alpha')
    plt.xlabel('Alpha')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('grafico_regularizacao.png')

if __name__ == "__main__":
    executar_regressao_multipla()