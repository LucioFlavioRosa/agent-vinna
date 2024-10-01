
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    orders = pd.read_sql_query("SELECT id_produto, quantidade_do_produto_vendida FROM orders WHERE data_da_compra >= '2024-07-01' AND data_da_compra < '2024-08-01'", engine)
    products = pd.read_sql_query("SELECT id_produto, subgrupo_do_produto FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('subgrupo_do_produto').apply(lambda x: (x['quantidade_do_produto_vendida']).sum()).reset_index(name='total_vendas')
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='total_vendas', y='subgrupo_do_produto', ax=ax)
    return fig
