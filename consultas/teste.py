
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    
    query_orders = "SELECT * FROM orders WHERE data_da_compra >= '2023-07-01' AND data_da_compra < '2023-08-01'"
    orders = pd.read_sql_query(query_orders, engine)
    
    query_products = "SELECT * FROM products"
    products = pd.read_sql_query(query_products, engine)
    
    merged_data = orders.merge(products, on='id_produto')
    
    faturamento_julho = merged_data.groupby(['subgrupo_do_produto']) \
                                   .apply(lambda x: (x['preco_unitario'] * x['quantidade_do_produto_vendida']).sum()) \
                                   .reset_index(name='faturamento')
    
    faturamento_julho['subgrupo_do_produto'] = faturamento_julho['subgrupo_do_produto'].astype(str)
    
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    plt.pie(faturamento_julho['faturamento'], labels=faturamento_julho['subgrupo_do_produto'], autopct='%1.1f%%')
    plt.title('Faturamento de Julho de 2024 por Subgrupo - Grupo Padaria')
    
    plt.savefig('resultado_python/grafico_faturamento_julho_2024.png')
    plt.close()
    
    return 'grafico_faturamento_julho_2024.png'
