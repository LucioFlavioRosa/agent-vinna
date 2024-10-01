
import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt

def estimativa():
    engine = sqlalchemy.create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT id_produto, preco_unitario, quantidade_do_produto_vendida FROM orders", engine)
    products = pd.read_sql_query("SELECT id_produto, grupo_do_produto FROM products", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    merged_data['faturamento'] = merged_data['preco_unitario'] * merged_data['quantidade_do_produto_vendida']
    faturamento_por_grupo = merged_data.groupby('grupo_do_produto')['faturamento'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=faturamento_por_grupo, x='faturamento', labels=faturamento_por_grupo['grupo_do_produto'])
    return fig
