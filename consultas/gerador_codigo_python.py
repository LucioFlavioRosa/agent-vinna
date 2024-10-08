import os
import json
import time
import datetime
import inspect

from openai import OpenAI
from github import Github

from conferencia import confere_python

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_NAME = "gpt-4o-mini"
openai_client = OpenAI(api_key=OPENAI_API_KEY)
current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def execute_python_code(code_string):
    """
    Executes a Python code string and returns the results (if any).

    Args:
        code_string: The Python code as a string.

    Returns:
        A dictionary containing the results of the code execution, 
        including any variables or objects created.
    """

    # Create a dictionary to store the results
    results = {}

    # Define a function to capture variables created during execution
    def capture_locals(local_vars):
        results.update(local_vars)

    # Execute the code string, passing the 'capture_locals' function as the 'locals' argument
    exec(code_string, globals(), capture_locals)

    return results

def generate_code(pergunta: str,
                  descricao_tabelas: str,
                  nome_colunas: str,
                  tipo_colunas: str,
                  descricao_colunas: str,
                  detalhes: str,
                  codigo_anterior: str,
                  feedback: str,
                  erro_extra: str) -> str:
    """
    Generates SQL queries from natural language questions using OpenAI.

    Returns:
        str: The generated SQL query.
    """

    prompt = [{"role": "system",
               "content": " Você é um especialista na escrita de códigos Python, me ajude na tarefa"},
              {'role': 'user',
               'content': pergunta},
              {'role': 'assistant',
               'content': 'as tabelas disponiveis sao: ' + descricao_tabelas},
              {'role': 'assistant',
               'content': 'com as colunas: ' + nome_colunas},
              {'role': 'assistant',
               'content': 'que sao dos tipos: ' + tipo_colunas},
              {'role': 'assistant',
               'content': 'que tem as seguintes caracristicas: ' + descricao_colunas},
              {'role': 'assistant',
               'content': 'deve seguir as instrucoes: ' + detalhes},
              {'role': 'assistant',
               'content': 'o codigo gerado anteriormente foi: ' + codigo_anterior},
              {'role': 'assistant',
               'content': 'e o motivo do erro foi: ' + feedback},
              {'role': 'assistant',
               'content': 'EVITE ESSE ERRO: ' + erro_extra}]


    response = openai_client.chat.completions.create(model=MODEL_NAME,
                                                     messages=prompt,
                                                     temperature=0.4,
                                                     max_tokens=1000)
    codigo_final = response.choices[0].message.content.strip().replace(
        "```python", "").replace(
        '```', '')

    return codigo_final



def query_selection(pergunta: str,
                    queries: str) -> str:
    prompt = [{"role": "system",
               "content": "Eu tenho um conjunto de queries que podem ajudar a responder uma pergunta, sua tarefa é "
                          "definir qual query tem maior chance de ajudar a responder a pergunta feita"},
              {'role': 'user',
               'content': pergunta},
              {'role': 'assistant',
               'content': 'as queries são' + queries},
              {'role': 'assistant',
               'content': 'a respota final deve ser somente o nome da query:'},
              {"role": "user",
               "content": "A query que melhor responde a pergunta feita é:"}
              ]

    response = openai_client.chat.completions.create(model=MODEL_NAME,
                                                     messages=prompt,
                                                     temperature=0.2,
                                                     max_tokens=10)

    resposta = response.choices[0].message.content.strip()

    return resposta


def main(pergunta: str,
         descricao_tabelas: str,
         nome_colunas: str,
         tipo_colunas: str,
         descricao_colunas: str,
         detalhes: dict):

    selected_query = query_selection(pergunta=pergunta,
                                     queries=json.dumps(detalhes))

    erro_extra = ''
    while True:
        try:
            codigo_anterior = ''
            analise = ''
            response = False
            while not response:
                codigo_final = generate_code(pergunta=pergunta,
                                             descricao_tabelas=descricao_tabelas,
                                             nome_colunas=nome_colunas,
                                             tipo_colunas=tipo_colunas,
                                             descricao_colunas=descricao_colunas,
                                             detalhes=json.dumps(detalhes[selected_query]),
                                             codigo_anterior=codigo_anterior,
                                             feedback=analise,
                                             erro_extra=erro_extra)

                codigo_anterior = codigo_final

                analise = confere_python.check_code(codigo=codigo_final,
                                                    descricao_tabelas=descricao_tabelas,
                                                    nome_colunas=nome_colunas,)

                if 'yes' or 'correto' in analise.lower():
                    response = True
                else:
                    response = False
          
            resultado = codigo_final
            break
          
        except Exception as e:
          print("An error occurred:", str(e))
          continue  
      
    return resultado
