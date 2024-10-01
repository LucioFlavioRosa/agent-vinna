import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_NAME = "gpt-4o-mini"
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def lowercase_list(input_list):
    """Converts all letters in a list to lowercase.

  Args:
      input_list: The list containing strings.

  Returns:
      A new list with all letters converted to lowercase.
  """
    output_list = []
    for item in input_list:
        if isinstance(item, str):
            output_list.append(item.lower())
        else:
            output_list.append(item)  # Keep non-string items as is
    return output_list


def find_relevant_tables(pergunta: str,
                         descricao_tabelas: str,
                         nome_colunas: str,
                         descricao_colunas: str,
                         detalhes: str) -> list:
    """
    Identifies tables relevant to a given question, considering that the answer might require multiple tables.

    Args:
        .


    Returns:
        A list of table names that might answer the question, potentially including multiple tables if needed.

    """

    # Construct the prompt for OpenAI
    prompt = [{"role": "system",
               "content": "You are an expert that helps to define which tables are relevant to answer the question.", },
              {'role': 'user',
               'content': pergunta},
              {'role': 'assistant',
               'content': 'as tabelas disponiveis sao: ' + descricao_tabelas},
              {'role': 'assistant',
               'content': 'com as seguinte colunas: ' + nome_colunas},
              {'role': 'assistant',
               'content': 'que tem as seguintes caracristicas: ' + descricao_colunas},
              {'role': 'assistant',
               'content': 'deve seguir as instrucoes: ' + detalhes},
              {"role": "user", "content": "the final result have to be a list with the name of the tables?"}]

    # Extract and return the relevant table names
    response = openai_client.chat.completions.create(model=MODEL_NAME,
                                                     messages=prompt,
                                                     temperature=0.2,
                                                     max_tokens=100)
    relevant_tables = response.choices[0].message.content.strip()

    # Split if multiple tables are suggested
    if "," in relevant_tables:
        relevant_tables = [table.strip() for table in relevant_tables.split(",")]
    else:
        relevant_tables = [relevant_tables]

    final_list = lowercase_list(relevant_tables)

    return final_list


def selecao_tabelas(pergunta,
                    tabelas,
                    nome_colunas,
                    descricao_colunas,
                    detalhes,
                    tentativas) -> list:
    customers = 0
    orders = 0
    products = 0
    reviews = 0

    for i in range(0, tentativas):
        relevant_tables = find_relevant_tables(pergunta=pergunta,
                                               descricao_tabelas=tabelas,
                                               nome_colunas=nome_colunas,
                                               descricao_colunas=descricao_colunas,
                                               detalhes=detalhes
                                               )
        for element in relevant_tables:
            if 'customers' in element:
                customers = customers + 1
            if 'orders' in element:
                orders = orders + 1
            if 'products' in element:
                products = products + 1
            if 'reviews' in element:
                reviews = reviews + 1

    resultado_final_tabelas = {'customers': customers, 'orders': orders, 'products': products, 'reviews': reviews}

    lista_tabelas = []
    for tabela in resultado_final_tabelas.keys():
        if resultado_final_tabelas[tabela] > int(tentativas / 2) + 1:
            lista_tabelas.append(tabela)

    return lista_tabelas
