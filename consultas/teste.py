Aqui está o código que atende a todas as suas instruções:


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
 sns.barplot(x='mes', y='faturamento', data=df)
 plt.xlabel('Mês')
 plt.ylabel('Faturamento')
 plt.title('Faturamento Mensal de 2023')
 return plt.show()
 

Esse código lê os dados da tabela `orders`, calcula o faturamento mensal de 2023 e gera um gráfico de barras usando a biblioteca Seaborn.