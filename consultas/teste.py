
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    query = """
    SELECT DATE_TRUNC('year', data_da_compra) AS ano, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
    FROM orders
    GROUP BY ano
    ORDER BY ano;
    """
    df = pd.read_sql_query(query, engine)
    fig, ax = plt.subplots()
    sns.barplot(x='ano', y='faturamento', data=df, ax=ax)
    ax.set_title('Faturamento Anual')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Faturamento')
    return fig
