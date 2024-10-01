
import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt

def estimativa():
 engine = sqlalchemy.create_engine(os.environ['banco_sql_postgresql'])
 orders = pd.read_sql_query("SELECT data_da_compra, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento FROM orders WHERE data_da_compra >= '2023-01-01' AND data_da_compra < '2024-01-01' GROUP BY data_da_compra ORDER BY data_da_compra", engine)
 orders['mes'] = orders['data_da_compra'].dt.to_period('M')
 monthly_revenue = orders.groupby('mes')['faturamento'].sum().reset_index()
 fig, ax = plt.subplots()
 sns.barplot(x='mes', y='faturamento', data=monthly_revenue, ax=ax)
 return fig
