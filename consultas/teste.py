
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
import os

def estimativa():
    engine = sqlalchemy.create_engine(os.getenv('banco_sql_postgresql'))
    query = """
    SELECT DATE_TRUNC('month', data_da_compra) AS mes, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
    FROM orders
    WHERE DATE_PART('year', data_da_compra) = 2023
    GROUP BY mes
    ORDER BY mes;
    """
    df = pd.read_sql_query(query, engine)
    fig, ax = plt.subplots()
    sns.barplot(x='mes', y='faturamento', data=df, ax=ax)
    ax.set_title('Faturamento Mensal em 2023')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Faturamento')
    return fig
