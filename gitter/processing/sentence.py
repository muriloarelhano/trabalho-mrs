from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


def generate_sentiment_label(p_pos):
    if p_pos >= 0.90:
        return 'positive'
    if p_pos >= 0.60 and p_pos < 0.90:
        return 'slightly_positive'
    if p_pos < 0.60 and p_pos >= 0.40:
        return 'neutral'
    if p_pos < 0.40 and p_pos > 0.10:
        return 'slightly_negative'
    if p_pos <= 0.10:
        return 'negative'


def apply_sentimental_analysis(df):
    for i, row in df.iterrows():

        sentence = TextBlob(df.at[i, "sentence"],
                            analyzer=NaiveBayesAnalyzer())

        df.at[i, "sentiment_label"] = generate_sentiment_label(
            sentence.sentiment.p_pos)

        df.at[i, "sentiment"] = sentence.sentiment.classification
        df.at[i, "pos"] = sentence.sentiment.p_pos
        df.at[i, "neg"] = sentence.sentiment.p_neg

    return df
