pontoA =(1, 2)
pontoB =(4, 6)
def distancia_pontos(pA, pB):
    return ((pB[0] - pA[0]) ** 2 + (pB[1] - pA[1]) ** 2) ** 0.5
distancia = distancia_pontos(pontoA, pontoB)
print(f"A distância entre os pontos A{pontoA} e B{pontoB} é: {distancia:.2f}")
