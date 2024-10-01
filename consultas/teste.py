
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    orders = pd.read_sql_query("SELECT * FROM orders WHERE data_da_compra >= '2023-07-01' AND data_da_compra < '2023-08-01'", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').apply(lambda x: (x['preco_unitario'] * x['quantidade_do_produto_vendida']).sum()).reset_index(name='faturamento')
    faturamento = faturamento.sort_values(by='faturamento', ascending=False)
    faturamento['cumulative'] = faturamento['faturamento'].cumsum()
    faturamento['cumulative_percentage'] = faturamento['cumulative'] / faturamento['faturamento'].sum() * 100
    fig, ax = plt.subplots()
    sns.barplot(x='grupo_do_produto', y='faturamento', data=faturamento, ax=ax)
    ax2 = ax.twinx()
    sns.lineplot(x='grupo_do_produto', y='cumulative_percentage', data=faturamento, ax=ax2, color='r', marker='o')
    ax2.axhline(80, ls='--', color='gray')
    ax.set_ylabel('Faturamento')
    ax2.set_ylabel('Porcentagem Cumulativa')
    ax.set_xlabel('Grupo de Produto')
    return fig
