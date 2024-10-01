import json

from consultas import gerador_query_sql, sql_query_python_code_or_tables, gerador_codigo_python
from utilidades import leitura_yaml_files, selecao_tabelas


def main(question):
    tabelas = leitura_yaml_files.leitura(arquivo='descricao_tabelas.yaml')['dados']
    nome_colunas = leitura_yaml_files.leitura(arquivo='nome_colunas.yaml')['dados']
    tipo_colunas = leitura_yaml_files.leitura(arquivo='tipo_colunas.yaml')['dados']
    descricao_colunas = leitura_yaml_files.leitura(arquivo='descricao_colunas.yaml')['dados']
    definicoes_de_negocio = leitura_yaml_files.leitura(arquivo='definicoes_de_negocio.yaml')['dados']
    codigo_python = leitura_yaml_files.leitura(arquivo='queries_para_gerar_codigo.yaml')

    melhor_caminho = sql_query_python_code_or_tables.resposta(pergunta=question)

    lista_tabelas = selecao_tabelas.selecao_tabelas(pergunta=question,
                                                    tabelas=json.dumps(tabelas),
                                                    nome_colunas=json.dumps(nome_colunas),
                                                    descricao_colunas=json.dumps(descricao_colunas),
                                                    detalhes=json.dumps(definicoes_de_negocio),
                                                    tentativas=5)
    tabelas_selecionadas = {}
    colunas_selecionadas = {}
    tipo_de_colunas = {}
    desc_col_selecionadas = {}

    for table in lista_tabelas:
        tabelas_selecionadas[table] = tabelas[table]
        colunas_selecionadas[table] = nome_colunas[table]
        tipo_de_colunas[table] = tipo_colunas[table]
        desc_col_selecionadas[table] = descricao_colunas[table]

    if 'sql' in melhor_caminho.lower():
        resultado_final = gerador_query_sql.main(pergunta=question,
                                                 descricao_tabelas=json.dumps(tabelas_selecionadas),
                                                 nome_colunas=json.dumps(colunas_selecionadas),
                                                 tipo_colunas=json.dumps(tipo_de_colunas),
                                                 descricao_colunas=json.dumps(desc_col_selecionadas),
                                                 conceitos_de_negocio=json.dumps(definicoes_de_negocio))

    else:
        resultado_final = gerador_codigo_python.main(pergunta=question,
                                                     descricao_tabelas=json.dumps(tabelas_selecionadas),
                                                     nome_colunas=json.dumps(colunas_selecionadas),
                                                     tipo_colunas=json.dumps(tipo_de_colunas),
                                                     descricao_colunas=json.dumps(desc_col_selecionadas),
                                                     detalhes=codigo_python)



    return resultado_final
