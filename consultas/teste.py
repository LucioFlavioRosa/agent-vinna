
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    
    query_orders = "SELECT * FROM orders WHERE data_da_compra >= '2023-07-01' AND data_da_compra < '2023-08-01'"
    query_products = "SELECT * FROM products"
    
    orders = pd.read_sql_query(query_orders, engine)
    products = pd.read_sql_query(query_products, engine)
    
    merged_data = pd.merge(orders, products, on='id_produto')
    
    faturamento_julho = merged_data.groupby(['subgrupo_do_produto']) \
                                   .apply(lambda x: (x['preco_unitario'] * x['quantidade_do_produto_vendida']).sum()) \
                                   .reset_index(name='faturamento')
    
    faturamento_julho['subgrupo_do_produto'] = faturamento_julho['subgrupo_do_produto'].astype(str)
    
    model = Prophet()
    model.fit(faturamento_julho.rename(columns={'subgrupo_do_produto': 'ds', 'faturamento': 'y'}))
    
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=faturamento_julho, x='subgrupo_do_produto', y='faturamento')
    plt.title('Faturamento por Subgrupo - Julho de 2024')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('resultado_python/faturamento_julho_2024.png')
    
    return 'faturamento_julho_2024.png'
