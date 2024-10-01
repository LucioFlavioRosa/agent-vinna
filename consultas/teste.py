
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT id_produto, preco_unitario, quantidade_do_produto_vendida, data_da_compra FROM orders WHERE data_da_compra >= '2023-07-01' AND data_da_compra < '2023-08-01'", engine)
    products = pd.read_sql_query("SELECT id_produto, grupo_do_produto FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    merged_data['faturamento'] = merged_data['preco_unitario'] * merged_data['quantidade_do_produto_vendida']
    faturamento_por_grupo = merged_data.groupby('grupo_do_produto')['faturamento'].sum().reset_index()
    faturamento_por_grupo = faturamento_por_grupo.sort_values(by='faturamento', ascending=False)
    faturamento_por_grupo['cumulative'] = faturamento_por_grupo['faturamento'].cumsum()
    faturamento_por_grupo['cumulative_percentage'] = 100 * faturamento_por_grupo['cumulative'] / faturamento_por_grupo['faturamento'].sum()
    fig, ax = plt.subplots()
    sns.barplot(x='grupo_do_produto', y='faturamento', data=faturamento_por_grupo, ax=ax)
    ax2 = ax.twinx()
    sns.lineplot(x='grupo_do_produto', y='cumulative_percentage', data=faturamento_por_grupo, ax=ax2, color='r', marker='o')
    ax2.axhline(80, ls='--', color='gray')
    ax.set_ylabel('Faturamento')
    ax2.set_ylabel('Cumulative Percentage')
    ax.set_xlabel('Grupo de Produto')
    return fig
