
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    query_orders = "SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) as faturamento FROM orders WHERE data_da_compra >= '2023-07-01' AND data_da_compra < '2024-08-01' GROUP BY data_da_compra ORDER BY data_da_compra"
    df_orders = pd.read_sql_query(query_orders, engine)
    
    df_orders['data_da_compra'] = pd.to_datetime(df_orders['data_da_compra'])
    df_orders.rename(columns={'data_da_compra': 'ds', 'faturamento': 'y'}, inplace=True)
    
    model = Prophet()
    model.fit(df_orders)
    
    future = model.make_future_dataframe(periods=31)
    forecast = model.predict(future)
    
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=forecast, x='ds', y='yhat', label='Estimativa de Faturamento')
    plt.title('Estimativa de Faturamento para Julho de 2024')
    plt.xlabel('Data')
    plt.ylabel('Faturamento')
    plt.legend()
    plt.savefig('resultado_python/estimativa_faturamento_julho_2024.png')
    
    return 'estimativa_faturamento_julho_2024.png'
