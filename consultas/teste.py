
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    query_orders = "SELECT id_produto, quantidade_do_produto_vendida, data_da_compra FROM orders WHERE data_da_compra >= '2023-05-01' AND data_da_compra < '2023-06-01'"
    query_products = "SELECT id_produto, grupo_do_produto FROM products"
    orders = pd.read_sql_query(query_orders, engine)
    products = pd.read_sql_query(query_products, engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').apply(lambda x: (x['quantidade_do_produto_vendida'] * x['preco_unitario']).sum()).reset_index(name='faturamento')
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='faturamento', labels=faturamento['grupo_do_produto'])
    return fig
