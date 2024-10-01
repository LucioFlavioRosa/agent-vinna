
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT id_produto, preco_unitario, quantidade_do_produto_vendida FROM orders", engine)
    products = pd.read_sql_query("SELECT id_produto, grupo_do_produto FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    merged_data['faturamento'] = merged_data['preco_unitario'] * merged_data['quantidade_do_produto_vendida']
    faturamento_por_grupo = merged_data.groupby('grupo_do_produto')['faturamento'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(faturamento_por_grupo['faturamento'], labels=faturamento_por_grupo['grupo_do_produto'], autopct='%1.1f%%')
    return fig
