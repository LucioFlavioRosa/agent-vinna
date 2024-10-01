
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    query = """
    SELECT 
        DATE_TRUNC('month', data_da_compra) AS mes,
        SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
    FROM 
        orders
    WHERE 
        data_da_compra >= '2024-01-01' AND data_da_compra < '2024-08-01'
    GROUP BY 
        mes
    ORDER BY 
        mes;
    """
    df = pd.read_sql_query(query, engine)
    fig, ax = plt.subplots()
    ax.pie(df['faturamento'], labels=df['mes'].dt.strftime('%B'), autopct='%1.1f%%')
    ax.set_title('Faturamento Mensal de Janeiro a Julho de 2024')
    return fig
