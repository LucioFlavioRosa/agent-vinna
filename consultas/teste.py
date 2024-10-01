
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged = pd.merge(orders, products, on='id_produto')
    merged['faturamento'] = merged['preco_unitario'] * merged['quantidade_do_produto_vendida']
    faturamento_por_subgrupo = merged.groupby('subgrupo_do_produto')['faturamento'].sum()
    fig, ax = plt.subplots()
    ax.pie(faturamento_por_subgrupo, labels=faturamento_por_subgrupo.index, autopct='%1.1f%%')
    return fig
