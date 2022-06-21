# %%
import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from gitter.messages import process_messages
from gitter.processing.sentence import apply_sentence_correction, apply_sentence_normalization, remove_stop_words
from gitter.scraper import GitterScraper

try:
    scraper = GitterScraper(
        "62fe76c279230fbd70415c924fef5d1b26f1aec7", "555f74e315522ed4b3e0ce42"
    )
    messages = scraper.get_messages(100, 5000)

except ValueError:
    print(f'Error with gitter API')

# %%

remove_columns = ["text", "status", "v", "editedAt",
                  "threadMessageCount", "readBy", "unread"]

messages_df = pd.DataFrame(process_messages(messages)).drop(
    columns=remove_columns, errors="ignore")
messages_df.rename(columns={'html': 'sentence'}, inplace=True)

messages_df = apply_sentence_normalization(messages_df)

messages_df = apply_sentence_correction(messages_df)

# messages_df['sentence'] = messages_df['sentence'].apply(remove_stop_words)

messages_df.reset_index(drop=True, inplace=True)

messages_df.to_csv('./database.csv', index=False)

print(messages_df.head())

#%%

# for i, row in messages_df.iterrows():
#     sentence = TextBlob(row["sentence"],  analyzer=NaiveBayesAnalyzer())
#     messages_df.at[i, "sentiment"] = sentence.sentiment.classification
#     messages_df.at[i, "pos"] = sentence.sentiment.p_pos
#     messages_df.at[i, "neg"] = sentence.sentiment.p_neg
#     print(messages_df.loc[i])

# print(messages_df.head())