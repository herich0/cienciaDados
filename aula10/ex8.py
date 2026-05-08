import time
from tqdm import tqdm

lista_itens = ['A', 'B', 'C', 'D', 'E']

for indice, item in enumerate(tqdm(lista_itens)):
    time.sleep(0.5)