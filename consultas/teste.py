Aqui está o código que atende às suas instruções:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os

def estimativa():
 engine = create_engine(os.getenv('banco_sql_postgresql'))
 query = """
 SELECT DATE_TRUNC('month', data_da_compra) AS mes, SUM(preco_unitario * quantidade_do_produto_vendida) AS faturamento
 FROM orders
 WHERE DATE_PART('year', data_da_compra) = 2023
 GROUP BY mes
 ORDER BY mes
 """
 df = pd.read_sql_query(query, engine)
 sns.barplot(x='mes', y='faturamento', data=df)
 plt.xticks(rotation=45)
 return plt.show()
