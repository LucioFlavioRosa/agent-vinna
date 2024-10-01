
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento FROM orders WHERE data_da_compra BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY data_da_compra", engine)
    orders['data_da_compra'] = pd.to_datetime(orders['data_da_compra'])
    fig, ax = plt.subplots()
    sns.lineplot(data=orders, x='data_da_compra', y='faturamento', ax=ax)
    return fig
