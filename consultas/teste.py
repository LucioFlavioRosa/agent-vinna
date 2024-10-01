
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    query_orders = "SELECT * FROM orders WHERE data_da_compra >= '2023-05-01' AND data_da_compra < '2023-06-01'"
    query_products = "SELECT * FROM products"
    orders = pd.read_sql_query(query_orders, engine)
    products = pd.read_sql_query(query_products, engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').agg({'preco_unitario': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='preco_unitario', labels=faturamento['grupo_do_produto'])
    return fig
