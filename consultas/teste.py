
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders WHERE DATE(data_da_compra) BETWEEN '2023-05-01' AND '2023-05-31'", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').agg({'preco_unitario': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='preco_unitario', labels=faturamento['grupo_do_produto'])
    return fig
