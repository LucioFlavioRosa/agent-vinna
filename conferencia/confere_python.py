import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_NAME = "gpt-4o-mini"
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def check_code(codigo: str,
               descricao_tabelas: str,
               nome_colunas: str) -> str:
    """
    Generates SQL queries from natural language questions using OpenAI.

    Returns:
        str: The generated SQL query.
    """

    prompt = [{"role": "system",
               "content": "você é um expert na escrita de codigo python, sua tarefa será conferir se a codigo "
                          "fornecido está correto"},
              {'role': 'user',
               'content': codigo},
              {'role': 'assistant',
               'content': 'as tabelas disponiveis sao: ' + descricao_tabelas},
              {'role': 'assistant',
               'content': 'com as seguinte colunas: ' + nome_colunas},
              {"role": "assistant", "content": "a resposta deve TER A PALAVRA YES para código que ESTIVER CORRETO"},
              {"role": "assistant", "content": "a resposta deve TER A PALAVRA NO para o código que APRESENTAR ALGUM ERRO"},
              {"role": "assistant", "content": "considere que o nome das tabelas e colunas sempre estão corretos"},
              {"role": "user", "content": "explique a resposta"}
              ]

    response = openai_client.chat.completions.create(model=MODEL_NAME,
                                                     messages=prompt,
                                                     temperature=0.5,
                                                     max_tokens=200)

    response = response.choices[0].message.content.strip()

    return response
