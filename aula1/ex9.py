class Produto:
    def __init__(self, nome, preco, estoque):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque

    def vender(self, quantidade):
        if quantidade <= self.estoque:
            self.estoque -= quantidade
            return True
        return False

    def repor_estoque(self, quantidade):
        self.estoque += quantidade

    def exibir_informacoes(self):
        print(f"Produto: {self.nome} | Preço: R${self.preco:.2f} | Estoque atual: {self.estoque} unidades")

produtoA = Produto("Monitor 24p", 850.00, 15)
produtoA.exibir_informacoes()

produtoA.vender(2)
produtoA.repor_estoque(5)
produtoA.exibir_informacoes()