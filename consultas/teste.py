
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    orders = pd.read_sql_query("SELECT * FROM orders", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby(['grupo_do_produto', 'subgrupo_do_produto'])['preco_unitario'].sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(faturamento['preco_unitario'], labels=faturamento['subgrupo_do_produto'], autopct='%1.1f%%')
    return fig
