
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    query_orders = "SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento FROM orders WHERE data_da_compra BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY data_da_compra"
    df = pd.read_sql_query(query_orders, engine)
    df['mes'] = pd.to_datetime(df['data_da_compra']).dt.to_period('M')
    faturamento_mensal = df.groupby('mes')['faturamento'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(x='mes', y='faturamento', data=faturamento_mensal, ax=ax)
    ax.set_title('Faturamento Mensal em 2023 do Grupo Padaria')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Faturamento')
    return fig
