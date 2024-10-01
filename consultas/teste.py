
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    query_orders = "SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) as faturamento FROM orders WHERE data_da_compra >= '2023-01-01' AND data_da_compra < '2024-08-01' GROUP BY data_da_compra ORDER BY data_da_compra"
    df_orders = pd.read_sql_query(query_orders, engine)

    df_orders['data_da_compra'] = pd.to_datetime(df_orders['data_da_compra'])
    df_orders.rename(columns={'data_da_compra': 'ds', 'faturamento': 'y'}, inplace=True)

    model = Prophet()
    model.fit(df_orders)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    monthly_forecast = forecast[['ds', 'yhat']].set_index('ds').resample('M').sum()

    plt.figure(figsize=(10, 6))
    plt.pie(monthly_forecast['yhat'], labels=monthly_forecast.index.strftime('%Y-%m'), autopct='%1.1f%%')
    plt.title('Faturamento Mensal Estimado de Janeiro a Julho de 2024')
    plt.savefig('resultado_python/faturamento_estimado.png')
    
    return 'faturamento_estimado.png'
