
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento FROM orders WHERE EXTRACT(YEAR FROM data_da_compra) = 2023 GROUP BY data_da_compra ORDER BY data_da_compra", engine)
    orders['mes'] = orders['data_da_compra'].dt.to_period('M')
    faturamento_mensal = orders.groupby('mes')['faturamento'].sum().reset_index()
    sns.barplot(x='mes', y='faturamento', data=faturamento_mensal)
    plt.title('Faturamento Mensal de 2023')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('resultado_python/faturamento_mensal_2023.png')
    plt.close()
    return 'resultado_python/faturamento_mensal_2023.png'
