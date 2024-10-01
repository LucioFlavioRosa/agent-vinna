
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders", engine)
    products = pd.read_sql_query("SELECT * FROM products WHERE grupo_do_produto = 'carro'", engine)
    merged = pd.merge(orders, products, on='id_produto')
    merged['faturamento'] = merged['preco_unitario'] * merged['quantidade_do_produto_vendida']
    faturamento_por_subgrupo = merged.groupby('subgrupo_do_produto')['faturamento'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento_por_subgrupo, x='faturamento', labels=faturamento_por_subgrupo['subgrupo_do_produto'])
    return fig
