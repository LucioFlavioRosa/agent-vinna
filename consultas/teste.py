Aqui está o código Python que atende a todas as suas instruções:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    limpeza_data = merged_data[merged_data['grupo_do_produto'] == 'limpeza']
    faturamento = limpeza_data.groupby('subgrupo_do_produto')['preco_unitario'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='preco_unitario', y='subgrupo_do_produto', ax=ax)
    return fig
 

Certifique-se de que as bibliotecas necessárias estão instaladas e que a variável de ambiente `banco_sql_postgresql` está configurada corretamente antes de executar o código.