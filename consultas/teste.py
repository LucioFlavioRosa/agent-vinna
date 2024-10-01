
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

def estimativa():
 engine = create_engine(os.getenv('banco_sql_postgresql'))
 orders = pd.read_sql_query("SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento FROM orders WHERE data_da_compra BETWEEN '2023-01-01' AND '2023-12-31' GROUP BY data_da_compra ORDER BY data_da_compra", engine)
 orders['mes'] = orders['data_da_compra'].dt.to_period('M')
 monthly_faturamento = orders.groupby('mes')['faturamento'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(x='mes', y='faturamento', data=monthly_faturamento, ax=ax)
ax.set_title('Faturamento Mensal de 2023')
ax.set_xlabel('Mes')
ax.set_ylabel('Faturamento')
return fig
