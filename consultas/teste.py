
import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt

def estimativa():
    engine = sqlalchemy.create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT id_produto, quantidade_do_produto_vendida FROM orders WHERE data_da_compra >= '2023-05-01' AND data_da_compra < '2023-06-01'", engine)
    products = pd.read_sql_query("SELECT id_produto, grupo_do_produto FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    faturamento = merged_data.groupby('grupo_do_produto').sum().reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento, x='quantidade_do_produto_vendida', labels=faturamento['grupo_do_produto'])
    return fig
