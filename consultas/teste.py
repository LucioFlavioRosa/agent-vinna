Aqui está o código que atende a todas as suas instruções:


import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt

def estimativa():
    engine = sqlalchemy.create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders WHERE data_da_compra >= '2023-05-01' AND data_da_compra < '2023-06-01'", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').agg({'preco_unitario': 'sum'}).reset_index()
    fig, ax = plt.subplots()
    sns.pie(faturamento['preco_unitario'], labels=faturamento['grupo_do_produto'], autopct='%1.1f%%', ax=ax)
    return fig
 

Certifique-se de ter as bibliotecas necessárias instaladas e que a variável de ambiente `banco_sql_postgresql` está configurada corretamente.