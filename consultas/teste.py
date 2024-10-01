
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders WHERE data_da_compra >= '2024-07-01' AND data_da_compra < '2024-08-01'", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby(['grupo_do_produto', 'subgrupo_do_produto'])['preco_unitario'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='preco_unitario', hue='subgrupo_do_produto', ax=ax)
    return fig
