
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    query = """
    SELECT DATE_TRUNC('month', data_da_compra) AS mes, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
    FROM orders
    WHERE EXTRACT(YEAR FROM data_da_compra) = 2023
    GROUP BY mes
    ORDER BY mes;
    """
    df = pd.read_sql_query(query, engine)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='mes', y='faturamento', data=df)
    plt.title('Faturamento Mensal de 2023')
    plt.xlabel('Mes')
    plt.ylabel('Faturamento (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('resultado_python/faturamento_mensal_2023.png')
    return 'resultado_python/faturamento_mensal_2023.png'
