
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query('SELECT * FROM orders', engine)
    products = pd.read_sql_query('SELECT * FROM products', engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    limpeza_data = merged_data[merged_data['grupo_do_produto'] == 'limpeza']
    faturamento = limpeza_data.groupby('subgrupo_do_produto').apply(lambda x: (x['preco_unitario'] * x['quantidade_do_produto_vendida']).sum()).reset_index(name='faturamento')
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='faturamento', y='subgrupo_do_produto', ax=ax)
    return fig
