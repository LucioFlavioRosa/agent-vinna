
import pandas as pd
from sqlalchemy import create_engine
from prophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders_query = "SELECT * FROM orders WHERE data_da_compra >= '2023-07-01' AND data_da_compra < '2023-08-01'"
    products_query = "SELECT * FROM products"

    orders = pd.read_sql_query(orders_query, engine)
    products = pd.read_sql_query(products_query, engine)

    merged_data = pd.merge(orders, products, on='id_produto')
    merged_data['faturamento'] = merged_data['preco_unitario'] * merged_data['quantidade_do_produto_vendida']
    faturamento_julho = merged_data.groupby(['subgrupo_do_produto', 'data_da_compra']).agg({'faturamento': 'sum'}).reset_index()

    daily_faturamento = faturamento_julho.groupby('data_da_compra').agg({'faturamento': 'sum'}).reset_index()
    daily_faturamento.columns = ['ds', 'y']

    model = Prophet()
    model.fit(daily_faturamento)

    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=forecast, x='ds', y='yhat')
    plt.title('Previsão de Faturamento Diário')
    plt.xlabel('Data')
    plt.ylabel('Faturamento')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('resultado_python/forecast_faturamento.png')
    return 'forecast_faturamento.png'
