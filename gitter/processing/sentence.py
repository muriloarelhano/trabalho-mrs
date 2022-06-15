import re
import numpy as np
import pandas as pd
from textblob import TextBlob
from bs4 import BeautifulSoup
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

def apply_sentence_normalization(messages_df):
    # removendo emojs com o formado :emoj:
    regex = r':[^:\s]*(?:::[^:\s]*)*:'
    re_express = re.compile(regex)
    messages_df['sentence'] = messages_df['sentence'].str.replace(re_express, '')

    # transformando as strings vazias em NaN para poder remover utilizando a função dropna() do pandas
    messages_df["sentence"].replace("", np.nan, inplace=True)
    messages_df.dropna(subset=["sentence"], inplace=True)

    # normalizando os dados
    messages_df['sentence'] = messages_df['sentence'].str.lower()

    # removendo a palavra que nomeia a room
    messages_df['sentence'] = messages_df['sentence'].str.replace('typescript', '')

    # convertendo ISO para Date
    messages_df['sent'] = pd.to_datetime(messages_df['sent'])

    return messages_df


# aplicando correção ortográfica nas sentenças
def correction(x):
    text = TextBlob(x)
    return "".join(text.correct())

def apply_sentence_correction(messages_df):
    messages_df['sentence'] = messages_df['sentence'].apply(correction)
    return messages_df


def remove_stop_words(text):
    nlp = English()

    my_doc = nlp(text)

    token_list = []
    for token in my_doc:
        token_list.append(token.text)

    from spacy.lang.en.stop_words import STOP_WORDS

    filtered_sentence =[] 

    for word in token_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word) 

    return " ".join(filtered_sentence)
