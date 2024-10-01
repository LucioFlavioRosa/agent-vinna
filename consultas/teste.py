
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
    
    merged_data['faturamento'] = merged_data['preco_unitario'] * merged_data['quantidade_do_produto_vendida']
    
    faturamento_julho = merged_data.groupby(['subgrupo_do_produto'])['faturamento'].sum().reset_index()
    
    faturamento_julho['ds'] = pd.to_datetime('2024-07-01')
    faturamento_julho['y'] = faturamento_julho['faturamento']
    
    model = Prophet()
    model.fit(faturamento_julho[['ds', 'y']])
    
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=faturamento_julho, x='subgrupo_do_produto', y='faturamento')
    plt.title('Faturamento por Subgrupo - Julho de 2024')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig('resultado_python/faturamento_julho_2024.png')
    plt.close()
    
    return 'faturamento_julho_2024.png'
