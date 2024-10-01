
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders WHERE DATE(data_da_compra) >= '2024-07-01' AND DATE(data_da_compra) <= '2024-07-31'", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby(['subgrupo_do_produto'])['preco_unitario', 'quantidade_do_produto_vendida'].sum().reset_index()
    faturamento['total'] = faturamento['preco_unitario'] * faturamento['quantidade_do_produto_vendida']
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='total', labels=faturamento['subgrupo_do_produto'])
    return fig
