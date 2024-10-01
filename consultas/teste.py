
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders", engine)
    products = pd.read_sql_query("SELECT * FROM products WHERE grupo_do_produto = 'limpeza'", engine)
    merged = pd.merge(orders, products, on='id_produto')
    merged['faturamento'] = merged['preco_unitario'] * merged['quantidade_do_produto_vendida']
    subgrupo_faturamento = merged.groupby('subgrupo_do_produto')['faturamento'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(subgrupo_faturamento['faturamento'], labels=subgrupo_faturamento['subgrupo_do_produto'], autopct='%1.1f%%')
    return fig
