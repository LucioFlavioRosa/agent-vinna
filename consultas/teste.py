
import pandas as pd
import sqlalchemy
import seaborn as sns
import matplotlib.pyplot as plt

def estimativa():
    engine = sqlalchemy.create_engine(os.getenv('banco_sql_postgresql'))
    orders = pd.read_sql_query("SELECT * FROM orders", engine)
    products = pd.read_sql_query("SELECT * FROM products WHERE grupo_do_produto = 'limpeza'", engine)
    merged_data = pd.merge(orders, products, on='id_produto')
    merged_data['faturamento'] = merged_data['preco_unitario'] * merged_data['quantidade_do_produto_vendida']
    subgrupos_faturamento = merged_data.groupby('subgrupo_do_produto')['faturamento'].sum().reset_index()
    fig, ax = plt.subplots()
    sns.pieplot(data=subgrupos_faturamento, x='faturamento', y='subgrupo_do_produto', ax=ax)
    return fig
