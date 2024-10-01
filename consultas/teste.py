
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT id_produto, quantidade_do_produto_vendida FROM orders WHERE data_da_compra BETWEEN '2023-05-01' AND '2023-05-31'", engine)
    products = pd.read_sql_query("SELECT id_produto, grupo_do_produto FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').sum().reset_index()
    fig, ax = plt.subplots()
    ax.pie(faturamento['quantidade_do_produto_vendida'], labels=faturamento['grupo_do_produto'], autopct='%1.1f%%')
    ax.set_title('Faturamento por Grupo de Produtos - Maio 2023')
    return fig
