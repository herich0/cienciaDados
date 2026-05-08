import numpy as np
from sklearn.preprocessing import StandardScaler

dados = np.array([[1.70, 65], 
                  [1.80, 80], 
                  [1.60, 55], 
                  [1.75, 70]])

scaler = StandardScaler()
dados_normalizados = scaler.fit_transform(dados)