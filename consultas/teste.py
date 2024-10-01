
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    
    query_orders = """
    SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS total_vendas
    FROM orders
    WHERE data_da_compra >= NOW() - INTERVAL '1 year 6 months'
    GROUP BY data_da_compra
    ORDER BY data_da_compra
    """
    
    df = pd.read_sql(query_orders, engine)
    df.rename(columns={'data_da_compra': 'ds', 'total_vendas': 'y'}, inplace=True)
    
    model = Prophet()
    model.fit(df)
    
    future = model.make_future_dataframe(periods=31)  # Previsão para 31 dias
    forecast = model.predict(future)
    
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(31)
