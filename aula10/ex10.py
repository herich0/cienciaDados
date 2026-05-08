import pandas as pd
import time
from tqdm import tqdm

tqdm.pandas(desc="Progresso Geral", position=0)

df = pd.DataFrame({'valores': [10, 20, 15, 30]})

def operacao_com_sub_barra(valor):
    for _ in tqdm(range(valor), desc=f"Processando {valor}", leave=False, position=1):
        time.sleep(0.05)
    return valor ** 2

df['valores_processados'] = df['valores'].progress_apply(operacao_com_sub_barra)