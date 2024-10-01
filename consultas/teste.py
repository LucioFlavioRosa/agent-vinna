
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    query_orders = "SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento FROM orders WHERE EXTRACT(YEAR FROM data_da_compra) = 2023 GROUP BY data_da_compra ORDER BY data_da_compra"
    df_orders = pd.read_sql_query(query_orders, engine)
    df_orders['data_da_compra'] = pd.to_datetime(df_orders['data_da_compra'])
    fig, ax = plt.subplots()
    sns.lineplot(data=df_orders, x='data_da_compra', y='faturamento', ax=ax)
    return fig
