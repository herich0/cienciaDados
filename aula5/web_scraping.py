import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extrair_h2_url(url):
    resposta = requests.get(url, verify=False)
    
    if resposta.status_code == 200:
        sopa = BeautifulSoup(resposta.text, 'html.parser')
        
        titulos_h2 = sopa.find_all('h2')
        
        for titulo in titulos_h2:
            print(titulo.get_text(strip=True))
    else:
        print("Falha ao acessar a página.")

extrair_h2_url('https://github.com/herich0/cienciaDados')