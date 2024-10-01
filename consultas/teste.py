
import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = sqlalchemy.create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders WHERE data_da_compra >= '2024-07-01' AND data_da_compra < '2024-08-01'", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby(['subgrupo_do_produto'])['preco_unitario', 'quantidade_do_produto_vendida'].sum().reset_index()
    faturamento['total'] = faturamento['preco_unitario'] * faturamento['quantidade_do_produto_vendida']
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='total', y='subgrupo_do_produto', ax=ax)
    return fig
