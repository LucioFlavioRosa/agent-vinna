
import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt
import os

def estimativa():
    engine = sqlalchemy.create_engine(os.environ['banco_sql_postgresql'])
    query = """
    SELECT DATE_TRUNC('month', data_da_compra) AS mes, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
    FROM orders
    WHERE data_da_compra >= '2023-01-01' AND data_da_compra < '2024-01-01'
    AND id_produto IN (SELECT id_produto FROM products WHERE grupo_do_produto = 'padaria')
    GROUP BY mes
    ORDER BY mes;
    """
    df = pd.read_sql_query(query, engine)
    fig, ax = plt.subplots()
    sns.barplot(x='mes', y='faturamento', data=df, ax=ax)
    ax.set_title('Faturamento Mensal de 2023 - Grupo Padaria')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Faturamento')
    return fig
