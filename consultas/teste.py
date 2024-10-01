
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT id_produto, quantidade_do_produto_vendida FROM orders", engine)
    products = pd.read_sql_query("SELECT id_produto, subgrupo_do_produto FROM products WHERE grupo_do_produto = 'limpeza'", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('subgrupo_do_produto').apply(lambda x: (x['quantidade_do_produto_vendida'] * x['preco_unitario']).sum()).reset_index(name='faturamento')
    plt.figure(figsize=(10, 6))
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='faturamento', y='subgrupo_do_produto', ax=ax)
    return fig
