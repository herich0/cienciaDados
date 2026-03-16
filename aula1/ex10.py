class Veiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def tipo_habilitacao(self):
        return "Categoria não definida"

class Carro(Veiculo):
    def tipo_habilitacao(self):
        return "Categoria B"

class Moto(Veiculo):
    def tipo_habilitacao(self):
        return "Categoria A"

veiculoA = Carro("Ford", "Focus")
veiculoB = Moto("Yamaha", "MT-07")

print(f"Veículo: {veiculoA.marca} {veiculoA.modelo} -> Exige: {veiculoA.tipo_habilitacao()}")
print(f"Veículo: {veiculoB.marca} {veiculoB.modelo} -> Exige: {veiculoB.tipo_habilitacao()}")