
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    
    query_orders = """
    SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS total_vendas
    FROM orders
    WHERE data_da_compra >= '2023-01-01' AND data_da_compra < '2024-07-01'
    GROUP BY data_da_compra
    ORDER BY data_da_compra
    """
    
    df_orders = pd.read_sql_query(query_orders, engine)
    df_orders['data_da_compra'] = pd.to_datetime(df_orders['data_da_compra'])
    df_orders = df_orders.rename(columns={'data_da_compra': 'ds', 'total_vendas': 'y'})
    
    model = Prophet(daily_seasonality=True)
    model.fit(df_orders)
    
    future = model.make_future_dataframe(periods=180)
    forecast = model.predict(future)
    
    monthly_forecast = forecast[['ds', 'yhat']].set_index('ds').resample('M').sum().reset_index()
    
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    plt.pie(monthly_forecast['yhat'], labels=monthly_forecast['ds'].dt.strftime('%b %Y'), autopct='%1.1f%%')
    plt.title('Faturamento Mensal Estimado de Janeiro a Julho de 2024')
    plt.savefig('resultado_python/grafico_faturamento.png')
    
    return 'grafico_faturamento.png'
