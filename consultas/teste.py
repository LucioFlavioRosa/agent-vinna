
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT id_produto, quantidade_do_produto_vendida FROM orders", engine)
    products = pd.read_sql_query("SELECT id_produto, subgrupo_do_produto FROM products WHERE grupo_do_produto = 'limpeza'", engine)
    merged = pd.merge(orders, products, on='id_produto')
    faturamento = merged.groupby('subgrupo_do_produto').agg({'quantidade_do_produto_vendida': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='quantidade_do_produto_vendida', labels=faturamento['subgrupo_do_produto'])
    return fig
