import os
import yaml

from pathlib import Path


def leitura(arquivo: str) -> dict:
    caminho = Path(__file__).parent
    arquivo_completo = caminho /"dados_adicionais" / arquivo
    if os.path.isfile(arquivo_completo):
        with open(arquivo_completo, 'r') as file:
            dados: dict = yaml.safe_load(file)
        return dados
    else:
        raise FileNotFoundError(f"No such file or directory: {arquivo}")
