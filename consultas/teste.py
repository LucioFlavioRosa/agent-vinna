
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

def estimativa():
    engine = create_engine(os.environ['banco_sql_postgresql'])
    query = """
    SELECT 
        EXTRACT(MONTH FROM o.data_da_compra) AS mes,
        SUM(o.preco_unitario * o.quantidade_do_produto_vendida) AS faturamento
    FROM 
        orders o
    JOIN 
        products p ON o.id_produto = p.id_produto
    WHERE 
        p.grupo_do_produto = 'carro' 
        AND o.data_da_compra >= '2023-01-01' 
        AND o.data_da_compra < '2024-01-01'
    GROUP BY 
        mes
    ORDER BY 
        mes;
    """
    df = pd.read_sql_query(query, engine)
    fig, ax = plt.subplots()
    sns.barplot(x=df['mes'], y=df['faturamento'], ax=ax)
    ax.set_title('Faturamento Mensal de 2023 para o Grupo Carro')
    ax.set_xlabel('Mês')
    ax.set_ylabel('Faturamento')
    return fig
