import os
import string

from difflib import SequenceMatcher
from openai import OpenAI

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_NAME = "gpt-4o-mini"
openai_client = OpenAI(api_key=OPENAI_API_KEY)


def find_similar_words(word_list, sentence, threshold=0.8):
    """
    Finds words in a sentence that are similar to words in a list, based on a similarity threshold.

    Args:
        word_list: A list of words to compare against.
        sentence: The sentence to search in.
        threshold: The minimum similarity ratio (0 to 1) for a word to be considered similar.

    Returns:
        A list of similar words found in the sentence.
    """

    # Preprocess the sentence (optional, but recommended)
    sentence = sentence.lower().translate(str.maketrans('', '', string.punctuation))

    similar_words = []
    for word in word_list:
        for sentence_word in sentence.split():
            similarity_ratio = SequenceMatcher(None, word.lower(), sentence_word).ratio()
            if similarity_ratio >= threshold:
                similar_words.append(sentence_word)
                break  # Avoid adding the same sentence word multiple times

    return similar_words


def take_the_path(pergunta: str) -> str:
    """
    Generates SQL queries from natural language questions using OpenAI.

    Returns:
        str: The generated SQL query.
    """
    prompt = [{"role": "system",
               "content": "You are an expert that helps to define if the best way to answer the question is query sql,"
                          "python code or tables.", },
              {'role': 'user',
               'content': pergunta},
              {'role': 'assistant',
               'content': 'The reponse have to be just: sql, python or tables'},
              {"role": "user", "content": "the response is:?"}
              ]

    response = openai_client.chat.completions.create(model=MODEL_NAME,
                                                     messages=prompt,
                                                     temperature=0.2,
                                                     max_tokens=5)
    resposta = response.choices[0].message.content.strip()

    return resposta


def resposta(pergunta: str) -> str:
    if len(find_similar_words(word_list=['projeção', 'estimativa', 'será',
                                         'grafico', 'plotar'],
                          sentence=pergunta)) > 0:
        return 'python'
    else:
        return take_the_path(pergunta=pergunta)