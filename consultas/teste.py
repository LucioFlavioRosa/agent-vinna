
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

def estimativa():
 engine = create_engine(os.getenv('banco_sql_postgresql'))
 orders = pd.read_sql_query("SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento FROM orders WHERE data_da_compra BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY data_da_compra ORDER BY data_da_compra", engine)
 orders['mes'] = orders['data_da_compra'].dt.to_period('M')
 monthly_faturamento = orders.groupby('mes')['faturamento'].sum().reset_index()
 sns.barplot(x='mes', y='faturamento', data=monthly_faturamento)
 plt.xticks(rotation=45)
 plt.title('Faturamento Mensal - 2023')
 plt.xlabel('Mes')
 plt.ylabel('Faturamento')
 return plt.show()
