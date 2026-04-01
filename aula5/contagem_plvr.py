import re
from collections import Counter

def contar_palavras(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        texto = arquivo.read().lower()
        
    palavras = re.findall(r'\b\w+\b', texto)
    
    contador = Counter(palavras)
    
    for palavra, frequencia in contador.most_common(10):
        print(f"{palavra}: {frequencia}")

contar_palavras('texto.txt')