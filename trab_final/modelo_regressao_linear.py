import json
import matplotlib.pyplot as plt
import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


def carregar_dados():
    with open("config.json", "r") as file:
        configuracoes_db = json.load(file)

    cnx = mysql.connector.connect(**configuracoes_db)
    query = "SELECT valor_dolar, indice_sp FROM economia_regional"
    df = pd.read_sql(query, cnx)
    cnx.close()
    return df


def executar_regressao_linear():
    df = carregar_dados()
    df = df.dropna()

    X = df[["valor_dolar"]]
    y = df["indice_sp"]

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    coef_angular = model.coef_[0]
    coef_linear = model.intercept_

    print("--- PARAMETROS ENCONTRADOS NO MODELO ---")
    print(f"Coeficiente Angular (Slope): {coef_angular:.4f}")
    print(f"Coeficiente Linear (Intercept): {coef_linear:.4f}")
    print(f"Erro Quadrático Médio (MSE): {mse:.4f}")
    print(f"Coeficiente de Determinação (R²): {r2:.4f}")

    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color="blue", alpha=0.4, label="Dados Reais (Histórico)")
    plt.plot(X, y_pred, color="red", linewidth=2.5, label="Reta de Regressão")
    plt.title("Regressão Linear Simples: Impacto do Dólar na Atividade Econômica")
    plt.xlabel("Valor do Dólar (R$)")
    plt.ylabel("Índice de Atividade Econômica (SP)")
    plt.legend()
    plt.grid(True)
    plt.savefig("grafico_regressao_linear.png")
    print("\nGráfico 'grafico_regressao_linear.png' salvo com sucesso!")


if __name__ == "__main__":
    executar_regressao_linear()