from collections import Counter

def contador_palavras(frase):
    palavras = frase.lower().replace('.', '').replace(',', '').split()
    contador = Counter(palavras)
    return contador.most_common(3)

texto = "O código Python é limpo. Python é simples e código limpo é bom."
top_3_palavras = contador_palavras(texto)
print(f"As 3 palavras mais frequentes na frase são: {top_3_palavras}")