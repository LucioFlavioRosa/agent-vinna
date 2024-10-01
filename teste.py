
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

def estimativa():
    engine = create_engine('postgresql://luciorosa:postgres@localhost:5432/postgres')
    
    orders = pd.read_sql_query("SELECT * FROM orders", engine)
    products = pd.read_sql_query("SELECT * FROM products", engine)
    customers = pd.read_sql_query("SELECT * FROM customers", engine)

    orders_products = pd.merge(orders, products, on='id_produto')
    
    hoje = datetime.now()

    tempo_relacionamento = customers[['id_consumidor', 'data_de_atualizacao_do_cadastro']].copy()
    tempo_relacionamento['tempo_relacionamento'] = (hoje - tempo_relacionamento['data_de_atualizacao_do_cadastro']).dt.days
    tempo_relacionamento = tempo_relacionamento[['id_consumidor', 'tempo_relacionamento']]

    quantidade_compras = orders[['id_consumidor', 'id_compra']].groupby('id_consumidor').id_compra.nunique().reset_index()
    quantidade_compras.columns = ['id_consumidor', 'quantidade_compras']

    quantidade_media_itens = orders.groupby(['id_consumidor', 'id_compra']).agg({'quantidade_do_produto_vendida': 'sum'}).reset_index()
    quantidade_media_itens = quantidade_media_itens.groupby('id_consumidor').quantidade_do_produto_vendida.mean().reset_index()
    quantidade_media_itens.columns = ['id_consumidor', 'quantidade_media_itens']

    produtos_unicos_comprados = orders.groupby('id_consumidor').id_produto.nunique().reset_index()
    produtos_unicos_comprados.columns = ['id_consumidor', 'produtos_unicos_comprados']

    orders['valor_compra'] = orders['preco_unitario'] * orders['quantidade_do_produto_vendida'] + orders['valor_frete']
    valor_media_compras = orders.groupby('id_consumidor').valor_compra.mean().reset_index()
    valor_media_compras.columns = ['id_consumidor', 'valor_media_compras']

    intervalo_medio_compras = orders.groupby('id_consumidor').data_da_compra.agg(['min', 'max', 'count']).reset_index()
    intervalo_medio_compras['intervalo_medio'] = (intervalo_medio_compras['max'] - intervalo_medio_compras['min']).dt.days / intervalo_medio_compras['count']
    intervalo_medio_compras = intervalo_medio_compras[['id_consumidor', 'intervalo_medio']]

    fracao_media_grupo = orders_products.groupby(['id_consumidor', 'grupo_do_produto']).size().groupby(level=0).apply(lambda x: x / float(x.sum())).unstack().fillna(0).reset_index()
    fracao_media_grupo.columns.name = None

    features = tempo_relacionamento.merge(quantidade_compras, on='id_consumidor', how='inner')
    features = features.merge(quantidade_media_itens, on='id_consumidor', how='inner')
    features = features.merge(produtos_unicos_comprados, on='id_consumidor', how='inner')
    features = features.merge(valor_media_compras, on='id_consumidor', how='inner')
    features = features.merge(intervalo_medio_compras, on='id_consumidor', how='inner')
    
    features = features.merge(fracao_media_grupo, on='id_consumidor', how='inner')

    features.to_csv('resultado_clusterizacao/features.csv')
