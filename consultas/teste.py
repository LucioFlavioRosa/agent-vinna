
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders_query = "SELECT * FROM orders WHERE data_da_compra >= '2023-01-01' AND data_da_compra < '2024-01-01'"
    products_query = "SELECT * FROM products WHERE grupo_do_produto = 'carro'"
    
    orders = pd.read_sql_query(orders_query, engine)
    products = pd.read_sql_query(products_query, engine)
    
    merged_data = pd.merge(orders, products, on='id_produto')
    merged_data['faturamento'] = merged_data['preco_unitario'] * merged_data['quantidade_do_produto_vendida']
    merged_data['mes'] = merged_data['data_da_compra'].dt.to_period('M')
    
    faturamento_mensal = merged_data.groupby('mes')['faturamento'].sum().reset_index()
    faturamento_mensal['mes'] = faturamento_mensal['mes'].dt.to_timestamp()
    
    fig, ax = plt.subplots()
    sns.barplot(x='mes', y='faturamento', data=faturamento_mensal, ax=ax)
    ax.set_title('Faturamento Mensal de 2023 para o Grupo Carro')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Faturamento')
    
    return fig
