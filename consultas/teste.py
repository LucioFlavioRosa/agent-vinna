
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    query = """
    SELECT DATE(data_da_compra) AS data_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
    FROM orders
    WHERE DATE(data_da_compra) BETWEEN '2023-01-01' AND '2023-12-31'
    GROUP BY DATE(data_da_compra)
    ORDER BY DATE(data_da_compra);
    """
    df = pd.read_sql_query(query, engine)
    fig, ax = plt.subplots()
    sns.lineplot(data=df, x='data_compra', y='faturamento', ax=ax)
    ax.set_title('Faturamento de 2023')
    ax.set_xlabel('Data')
    ax.set_ylabel('Faturamento')
    return fig
