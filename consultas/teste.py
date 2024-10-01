
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    query = """
    SELECT 
        DATE_TRUNC('month', o.data_da_compra) AS mes,
        SUM(o.preco_unitario * o.quantidade_do_produto_vendida) AS faturamento
    FROM 
        orders o
    JOIN 
        products p ON o.id_produto = p.id_produto
    WHERE 
        p.grupo_do_produto = 'padaria' AND 
        o.data_da_compra BETWEEN '2023-01-01' AND '2023-12-31'
    GROUP BY 
        mes
    ORDER BY 
        mes;
    """
    df = pd.read_sql_query(query, engine)
    fig, ax = plt.subplots()
    sns.barplot(x='mes', y='faturamento', data=df, ax=ax)
    ax.set_title('Faturamento Mensal em 2023 do Grupo Padaria')
    ax.set_xlabel('Mes')
    ax.set_ylabel('Faturamento')
    return fig
