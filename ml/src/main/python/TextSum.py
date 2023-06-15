import textwrap
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import sys
import nltk
nltk.download('punkt')

# Set the encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Set the stemmer
def get_stopwords_list(stop_file_path):
    """load stop words"""
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return list(frozenset(stop_set))


def _create_dictionary_table(text_string) -> dict:
    # Chỉnh đường dẫn này stopword
    stopwords_path = "/app/vietnamese-stopwords.txt"
    stopwords = get_stopwords_list(stopwords_path)
    words = word_tokenize(text_string)

    # reducing words to their root form
    stem = PorterStemmer()

    # creating dictionary for the word frequency table
    frequency_table = dict()
    for wd in words:
        wd = stem.stem(wd)
        if wd in stopwords:
            continue
        if wd in frequency_table:
            frequency_table[wd] += 1
        else:
            frequency_table[wd] = 1

    return frequency_table


def _calculate_sentence_scores(sentences, frequency_table) -> dict:
    # algorithm for scoring a sentence by its words
    sentence_weight = dict()

    for sentence in sentences:
        sentence_wordcount = len(word_tokenize(sentence))
        sentence_wordcount_without_stop_words = 0
        for word_weight in frequency_table:
            if word_weight in sentence.lower():
                sentence_wordcount_without_stop_words += 1
                if sentence[:7] in sentence_weight:
                    sentence_weight[sentence[:7]] += frequency_table[word_weight]
                else:
                    sentence_weight[sentence[:7]] = frequency_table[word_weight]

        sentence_weight[sentence[:7]] = sentence_weight[sentence[:7]] / sentence_wordcount_without_stop_words

    return sentence_weight


def _calculate_average_score(sentence_weight) -> int:
    # calculating the average score for the sentences
    sum_values = sum(sentence_weight.values())
    average_score = sum_values / len(sentence_weight)

    return average_score


def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= threshold:
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary


def summarize_text(text):
    # tokenizing the sentences
    sentences = sent_tokenize(text)

    # creating a dictionary for the word frequency table
    frequency_table = _create_dictionary_table(text)

    # algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    # getting the threshold
    threshold = _calculate_average_score(sentence_scores)

    # producing the summary
    article_summary = _get_article_summary(sentences, sentence_scores, threshold)

    return article_summary

import os
if __name__ == '__main__':

    text = os.environ.get("text")

    # Preprocess the input text
    text = text.lower()
    text = text.replace('\n', '.')
    text = text.strip()
    #print('văn bản gốc' + text)
    summary_results = summarize_text(text)

    # Wrap the content into multiple lines
    line_width = 100  # Adjust the line width as needed
    summary_results_breaks = textwrap.wrap(summary_results, width=line_width)

    # print('\nVăn bản tóm tắt:')
    # Print the content with line breaks
    for line in summary_results_breaks:
        print(line)
