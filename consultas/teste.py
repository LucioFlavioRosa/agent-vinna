
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query('SELECT * FROM orders', engine)
    products = pd.read_sql_query('SELECT * FROM products', engine)
    merged = pd.merge(orders, products, on='id_produto')
    faturamento = merged.groupby(['grupo_do_produto', 'subgrupo_do_produto']).agg({'preco_unitario': 'sum'}).reset_index()
    plt.figure(figsize=(8, 8))
    plt.pie(faturamento['preco_unitario'], labels=faturamento['subgrupo_do_produto'], autopct='%1.1f%%')
    fig, ax = plt.subplots()
    return fig
