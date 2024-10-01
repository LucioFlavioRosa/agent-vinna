
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    query = """
    SELECT DATE(data_da_compra) AS data, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
    FROM orders
    WHERE data_da_compra >= '2023-01-01' AND data_da_compra < '2024-07-01'
    GROUP BY DATE(data_da_compra)
    ORDER BY data;
    """
    df = pd.read_sql_query(query, engine)
    df.columns = ['ds', 'y']
    
    model = Prophet()
    model.fit(df)
    
    future = model.make_future_dataframe(periods=180)
    forecast = model.predict(future)
    
    monthly_faturamento = forecast[['ds', 'yhat']].set_index('ds').resample('M').sum()
    
    plt.figure(figsize=(10, 6))
    plt.pie(monthly_faturamento['yhat'], labels=monthly_faturamento.index.strftime('%Y-%m'), autopct='%1.1f%%')
    plt.title('Faturamento Mensal de Janeiro a Julho de 2024')
    
    plt.savefig('resultado_python/grafico_faturamento.png')
    return 'grafico_faturamento.png'
