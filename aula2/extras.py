import numpy as np
def criacaobasica():
    return np.arange(10)

def matrizbooleana():
    return np.ones((3, 3), dtype=bool)

def impares(arr):
    return arr[arr % 2 != 0]

def substituir_impares(arr):
    arr[arr % 2 != 0] = -1
    return arr

def matriz_aleatoria():
    return np.random.randint(1, 101, (5, 5))

def soma_por_coluna(matriz):
    return np.sum(matriz, axis=0)

def maximo_por_linha(matriz):
    return np.max(matriz, axis=1)

def broadcasting_simples():
    arr = np.arange(5)
    return arr + 2

def concatenacao():
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    return np.concatenate((arr1, arr2))

def inverter_array(arr):
    return np.flip(arr)

def temp_media():
    temperaturas = np.random.randint(-10, 35, 7)
    media = np.mean(temperaturas)
    print ("Temperaturas da semana:", temperaturas)
    print ("Temperatura média da semana:", media)
    print ("temperaturatura mais quente da semana:", np.max(temperaturas))
    return 

def vendas_mensais():
    vendas = np.random.randint(50, 201, (3,4))
    total_vendas = np.sum(vendas, axis=0)
    print (vendas)
    print ("Total de vendas por produto:")
    print (total_vendas)

def pontuacoes_teste():
    notas = np.array([75, 88, 92, 65, 70, 80, 95, 60, 85, 78])
    print("Pontuação mínima:", np.min(notas))
    print("Pontuação máxima:", np.max(notas))

def dados_sensores():
    leituras = np.random.rand(20)
    filtradas = leituras[leituras > 0.7]
    print("Leituras acima de 0.7:\n", filtradas)

def precos_acoes():
    precos = np.array([120.50, 121.00, 119.80, 122.30, 120.00])
    variacao = np.diff(precos) / precos[:-1] * 100
    print("Variação percentual diária:\n", variacao)

def matriz_identidade():
    return np.eye(4)

def zeros_e_uns():
    zeros = np.zeros((3, 3))
    uns = np.ones((2, 5))
    return zeros, uns

def redimensionar_imagem():
    arr = np.random.randint(0, 256, 25)
    return arr.reshape((5, 5))

def filtrar_pares():
    arr = np.arange(10)
    return arr[arr % 2 == 0]

def soma_acumulada():
    arr = np.array([1, 2, 3, 4, 5])
    return np.cumsum(arr)

def valores_unicos():
    arr = np.array([1, 2, 2, 3, 4, 4, 4, 5])
    return np.unique(arr)

def interpolacao_linear():
    return np.linspace(0, 10, 5)

def media_ponderada():
    notas = np.array([80, 90, 70])
    pesos = np.array([0.3, 0.5, 0.2])
    return np.average(notas, weights=pesos)

def transposicao_dados():
    matriz = np.array([[1, 2, 3], [4, 5, 6]])
    return np.transpose(matriz)

def inverter_eixos():
    matriz = np.arange(12).reshape((3, 4))
    return matriz[::-1, :]

def comparacao_elementos():
    a = np.array([1, 2, 3])
    b = np.array([3, 2, 1])
    return a == b

def mascara_condicao():
    arr = np.random.randint(0, 101, 10)
    mascara = arr > 50
    return arr, mascara

def contagem_valores():
    arr = np.array([1, 7, 3, 7, 5, 7])
    return np.count_nonzero(arr == 7)

def arredondamento():
    arr = np.array([1.23, 2.78, 3.50, 4.11])
    return np.round(arr)

def combinar_arrays():
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([4, 5, 6])
    return np.vstack((arr1, arr2))
