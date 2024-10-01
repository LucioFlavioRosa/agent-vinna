import re
import os
import datetime

import pandas as pd

from openai import OpenAI
from sqlalchemy import create_engine
from conferencia import confere_query

engine = create_engine(os.environ['banco_sql_postgresql'])

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_NAME = "gpt-4o-mini"
openai_client = OpenAI(api_key=OPENAI_API_KEY)
current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')


def remove_after_string_regex(text, delimiter):
    """Removes all characters after the first occurrence of the delimiter using regex."""
    pattern = re.escape(delimiter) + ".*"  # Escape delimiter and match everything after it
    return re.sub(pattern, "", text)


def generate_sql_query(pergunta: str,
                       descricao_tabelas: str,
                       nome_colunas: str,
                       tipo_colunas: str = None,
                       descricao_colunas: str = None,
                       conceitos_de_negocio: str = None,
                       query_anterior: str = None,
                       feedback: str = None) -> str:
    """
    Generates SQL queries from natural language questions using OpenAI.

    Returns:
        str: The generated SQL query.
    """

    prompt = [{"role": "system",
               "content": "You are an expert SQL query generator that generates accurate SQL query"},
              {'role': 'user',
               'content': pergunta},
              {'role': 'assistant',
               'content': 'as tabelas disponiveis sao: ' + descricao_tabelas},
              {'role': 'assistant',
               'content': 'com as seguinte colunas: ' + nome_colunas},
              {'role': 'assistant',
               'content': 'que sao dos tipos: ' + tipo_colunas},
              {'role': 'assistant',
               'content': 'que tem as seguintes caracristicas: ' + descricao_colunas},
              {'role': 'assistant',
               'content': 'para ajudar temos algumas definicoes: ' + conceitos_de_negocio},
              {'role': 'assistant',
               'content': 'a tentativa anteriro de query foi: ' + query_anterior},
              {'role': 'assistant',
               'content': 'a query anterior foi errada pois: ' + feedback},
              {"role": "user", "content": "the final result must have just the sql query"},
              {"role": "user", "content": "as datas devem ser comparadas como data e NAO como strings"},
              {"role": "user", "content": "query must be in  PostgreSQL ready to be executed"},
              {"role": "user", "content": "SQL Query?"}
              ]


    response = openai_client.chat.completions.create(model=MODEL_NAME,
                                                     messages=prompt,
                                                     temperature=0.8,
                                                     max_tokens=500)

    sql_query = response.choices[0].message.content.strip().replace('sql',
                                                                    '').replace("```",
                                                                                '')
    final_query = remove_after_string_regex(sql_query, '\n\n')

    return final_query


def resultado_consulta(consulta: str) -> pd.DataFrame:
    df = pd.read_sql_query(consulta, engine)
    engine.dispose()  # Good practice to close the connection when done

    return df


def main(pergunta: str,
         descricao_tabelas: str,
         nome_colunas: str,
         tipo_colunas: str = None,
         descricao_colunas: str = None,
         conceitos_de_negocio: str = None) -> pd.DataFrame:

    query_ref = ''
    analise = ''
    response = False
    while not response:
        query = generate_sql_query(pergunta, descricao_tabelas,
                                   nome_colunas, tipo_colunas,
                                   descricao_colunas, conceitos_de_negocio,
                                   query_anterior=query_ref,
                                   feedback=analise)
        query_ref = query
        analise = confere_query.check_query(query=query,
                                             descricao_tabelas=descricao_tabelas,
                                             nome_colunas=nome_colunas)

        if 'yes' in analise.lower():
            response = True
        else:
            response = False

    df = resultado_consulta(consulta=query)

    return df
