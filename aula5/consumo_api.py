import requests

def buscar_repositorios_github(topico):
    url = f"https://api.github.com/search/repositories?q={topico}&per_page=5"
    
    resposta = requests.get(url)
    
    if resposta.status_code == 200:
        dados = resposta.json()
        repositorios = dados.get('items', [])
        
        for repo in repositorios:
            nome = repo.get('name')
            url_repo = repo.get('html_url')
            print(f"Nome: {nome} - URL: {url_repo}")
    else:
        print("Erro na requisição à API.")

buscar_repositorios_github('data science')