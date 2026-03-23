import requests
import json

response = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php?name=Dark%20Magician")

print(response.status_code)

if response.status_code == 200:
    data = response.json()
    try:
        with open("data.json", "r") as json_file:
            existing_data = json.load(json_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open("data.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)
else:
    print("ERRO: ", response.status_code)

#dae parmeiras