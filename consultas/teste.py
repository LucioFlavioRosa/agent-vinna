
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders", engine)
    products = pd.read_sql_query("SELECT * FROM products WHERE grupo_do_produto = 'limpeza'", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    merged_data['faturamento'] = merged_data['preco_unitario'] * merged_data['quantidade_do_produto_vendida']
    subgrupo_faturamento = merged_data.groupby('subgrupo_do_produto')['faturamento'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(subgrupo_faturamento['faturamento'], labels=subgrupo_faturamento['subgrupo_do_produto'], autopct='%1.1f%%')
    return fig
