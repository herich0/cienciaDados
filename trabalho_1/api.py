#dae parmeiras
#dae shimira
import requests
import json

url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
input_carta = input("Digite o nome da carta: ")
parametros = {"name": input_carta}
response = requests.get(url, params=parametros)

if response.status_code == 200:
    data = response.json()
    carta = data["data"][0]
    print ("carta encontrada.")
    
    url_imagem = carta["card_images"][0]["image_url"]
    nome_imagem = f"{carta['id']}.jpg"
    
    resposta_imagem = requests.get(url_imagem)
    if resposta_imagem.status_code == 200:
        with open(nome_imagem, "wb") as f_imagem:
            f_imagem.write(resposta_imagem.content)

    informacoes_filtradas = {
        "id": carta["id"],
        "name": carta["name"],
        "type": carta["type"],
        "frameType": carta["frameType"],
        "desc": carta["desc"],
        "atk": carta.get("atk"),
        "def": carta.get("def"),
        "imagem_local": nome_imagem
    }

    try:
        with open("data.json", "r", encoding="utf-8") as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    ja_existe = False
    for item in existing_data:
        if item["id"] == informacoes_filtradas["id"]:
            ja_existe = True
            break
            
    if not ja_existe:
        existing_data.append(informacoes_filtradas)
        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump(existing_data, json_file, indent=4, ensure_ascii=False)
        print(f"A carta {carta['name']} foi adicionada com sucesso!")
    else:
        print(f"A carta {carta['name']} já está no arquivo. Nenhuma duplicata foi criada.")

    with open("data.json", "w", encoding="utf-8") as json_file:
        json.dump(existing_data, json_file, indent=4, ensure_ascii=False)

else:
    print("ERRO: ", response.status_code)