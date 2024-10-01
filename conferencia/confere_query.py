import os

from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_NAME = "gpt-4o-mini"
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def check_query(query: str,
                descricao_tabelas: str,
                nome_colunas: str
                ) -> str:
    """
    Generates SQL queries from natural language questions using OpenAI.

    Returns:
        str: The generated SQL query.
    """

    prompt = [{"role": "system",
               "content": "você é um expert na escrita de queries sql PostgreSQL, sua tarefa será conferir se a query "
                          "fornecida está correta"},
              {'role': 'user',
               'content': query},
              {'role': 'assistant',
               'content': 'as tabelas disponiveis sao: ' + descricao_tabelas},
              {'role': 'assistant',
               'content': 'com as seguinte colunas: ' + nome_colunas},
              {"role": "user", "content": "toda data e string na query sql deve seguir os exemplos, '2024-01-01, "
                                          "'carro'"},
              {"role": "user", "content": "a resposta deve TER YES para query que está escrita corretamente"},
              {"role": "user", "content": "a resposta deve TER NO para query que apresenta erro"},
              {"role": "user", "content": "explique a resposta"}
              ]

    response = openai_client.chat.completions.create(model=MODEL_NAME,
                                                     messages=prompt,
                                                     temperature=0.4,
                                                     max_tokens=200)


    response = response.choices[0].message.content.strip()

    return response
