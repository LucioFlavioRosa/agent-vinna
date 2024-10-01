
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
 engine = create_engine(os.getenv('banco_sql_postgresql'))
 query = """
 SELECT DATE_TRUNC('month', data_da_compra) AS mes, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
 FROM orders
 WHERE DATE_PART('year', data_da_compra) = 2023
 GROUP BY mes
 ORDER BY mes;
 """
 df = pd.read_sql_query(query, engine)
 sns.barplot(x='mes', y='faturamento', data=df)
 plt.xticks(rotation=45)
 plt.title('Faturamento Mensal - 2023')
 plt.xlabel('Mes')
 plt.ylabel('Faturamento')
 return plt.show()
