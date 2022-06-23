import re
import numpy as np
import pandas as pd
from copy import copy
from bs4 import BeautifulSoup
from textblob import TextBlob

def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")

    for data in soup(['style', 'script', 'a', 'code']):
        data.decompose()

    return ' '.join(soup.stripped_strings)

def process_messages(messages):
    copy_messages = copy(messages)
    for idx, message in enumerate(copy_messages):
        try:
            # Remove "\" from original message, this is a gitter problem
            message["html"] = message["html"].replace('\\', "")
            # Remove all tags for get only pure text
            messages[idx]["html"] = remove_tags(message["html"])
            for key in list(message):
                if type(message[key]) == dict or type(message[key]) == list:
                    del messages[idx][key]
        except:
            print('Erro com campo HTML no gitter: ', message)
            break

    return messages


def apply_sentence_normalization(df):
    # removendo emojs com o formado :emoji:
    regex = r':[^:\s]*(?:::[^:\s]*)*:'
    re_express = re.compile(regex)
    df['sentence'] = df['sentence'].str.replace(re_express, '')

    # normalizando os dados
    df['sentence'] = df['sentence'].str.lower()

    # removendo a palavra que nomeia a room
    df['sentence'] = df['sentence'].str.replace('typescript', '')

    # transformando as strings vazias em NaN para poder remover utilizando a fun  o dropna() do pandas
    df.replace("", np.nan, inplace=True)
    df.dropna(inplace=True)

    return df


def apply_messages_pre_processing(splited_df):
    try:
        # convertendo ISO para Date
        splited_df['sent'] = pd.to_datetime(splited_df['sent'])

        splited_df = apply_sentence_normalization(splited_df)

        splited_df["sentence"] = splited_df["sentence"].apply(
            lambda x: "".join(TextBlob(x).correct()))

        return splited_df
    except:
        print('ERRO')
