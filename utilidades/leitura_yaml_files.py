import os
import yaml

from pathlib import Path


def leitura(arquivo: str) -> dict:
    caminho = "mount/src/agent-vinna/dado_adicionais/"
    print(caminho)
    arquivo_completo = caminho + arquivo
    if os.path.isfile(arquivo_completo):
        with open(arquivo_completo, 'r') as file:
            dados: dict = yaml.safe_load(file)
        return dados
    else:
        raise FileNotFoundError(f"No such file or directory: {arquivo_completo}")
