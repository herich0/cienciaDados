import csv

def calcular_media_categoria(caminho_arquivo, categoria_alvo):
    total_preco = 0.0
    quantidade = 0

    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        
        for linha in leitor:
            if linha['categoria'] == categoria_alvo:
                total_preco += float(linha['preco'])
                quantidade += 1

    if quantidade > 0:
        media = total_preco / quantidade
        print(f"Preço médio da categoria '{categoria_alvo}': R$ {media:.2f}")
    else:
        print("Nenhum produto encontrado para esta categoria.")

calcular_media_categoria('dados.csv', 'Eletrônicos')