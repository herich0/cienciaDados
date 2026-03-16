import pandas as pd

iterador_blocos = pd.read_csv('dados_sensor_gigante.csv', sep=',', na_values=['NA', '-'], chunksize=10)

for i, bloco in enumerate(iterador_blocos, start=1):
    media_temp = bloco['temperatura'].mean()
    valores_ausentes = bloco['temperatura'].isna().sum()

    print(f"--- Bloco {i} ---")
    print(f"Temperatura Média: {media_temp:.2f}")
    print(f"Valores Ausentes na Temperatura: {valores_ausentes}")
    print("-" * 30, "\n")