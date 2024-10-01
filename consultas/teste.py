
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    orders = pd.read_sql_query("SELECT id_produto, quantidade_do_produto_vendida FROM orders WHERE data_da_compra >= '2023-05-01' AND data_da_compra < '2023-06-01'", engine)
    products = pd.read_sql_query("SELECT id_produto, grupo_do_produto FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').apply(lambda x: (x['quantidade_do_produto_vendida']).sum()).reset_index(name='faturamento')
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='faturamento', labels=faturamento['grupo_do_produto'])
    return fig
