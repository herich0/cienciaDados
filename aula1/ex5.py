contatos = {
    "João": "42 99999-9999",
    "Maria": "42 98888-8888",
    "Pedro": "42 97777-7777",
}
for nome in contatos:
    print(nome)

busca = input("Digite o nome do contato: ")
if busca in contatos:
    print(f"Telefone de {busca}: {contatos[busca]}")
else:
    print(f"Contato {busca} não encontrado.")