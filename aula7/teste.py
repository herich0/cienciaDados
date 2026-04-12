import mysql.connector
import json

with open('config.json', 'r') as file:
    config = json.load(file)

try:
    cnx = mysql.connector.connect(
        user=config['user'],
        password=config['password'],
        host=config['host'],
        database=config['database']
    )

    if cnx.is_connected():
        print("Conexão com o banco de dados 'teste' realizada com sucesso!")

    cnx.close()

except mysql.connector.Error as err:
    print(f"Erro ao conectar: {err}")