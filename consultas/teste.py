
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT id_produto, quantidade_do_produto_vendida FROM orders", engine)
    products = pd.read_sql_query("SELECT id_produto, grupo_do_produto FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').agg({'quantidade_do_produto_vendida': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='quantidade_do_produto_vendida', y='grupo_do_produto', ax=ax)
    return fig
