import numpy as np

vendas = np.random.randint(100, 501, 12)

matriz_vendas = vendas.reshape(3, 4)

vendas_por_semana = np.sum(matriz_vendas, axis=1)

media_por_dia = np.mean(matriz_vendas, axis=0)

dias_acima_400 = np.sum(matriz_vendas > 400)    

print("Matriz de Vendas (3 semanas x 4 dias):")
print(matriz_vendas)

print("\nVenda total por semana:")
print(vendas_por_semana)

print("\nMédia de vendas para cada dia da semana:")
print(media_por_dia)

print("\nQuantidade de dias com vendas > 400:")
print(dias_acima_400)