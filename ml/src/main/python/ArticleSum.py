# importing libraries
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
import bs4
import textwrap
from nltk.stem import PorterStemmer
import urllib.request
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
url = os.environ.get("url")
#url = "https://www.msn.com/vi-vn/news/national/mi%E1%BB%81n-b%E1%BA%AFc-c%C3%B3-th%E1%BB%83-%C4%91%C3%B3n-3-%C4%91%E1%BB%A3t-m%C6%B0a-d%C3%B4ng-l%E1%BB%9Bn-trong-th%C3%A1ng-n%C3%A0y/ar-AA1c8A4Y?ocid=msedgntp&cvid=92f7dc19e1e54efc80ab05f60610905e&ei=11"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
req = urllib.request.Request(url, headers=headers)

# fetching the content from the URL
fetched_data = urllib.request.urlopen(url)

article_read = fetched_data.read()

# parsing the URL content and storing in a variable
article_parsed = bs4.BeautifulSoup(article_read, 'html.parser')

# returning <p> tags
paragraphs = article_parsed.find_all('p')

article_content = ''

# Preprocess the input text
article_content = article_content.lower()
article_content = article_content.replace('\n', '. ')
article_content = article_content.strip()

# looping through the paragraphs and adding them to the variable
for p in paragraphs:
    article_content += p.text

# Wrap the content into multiple lines
line_width = 100  # Adjust the line width as needed
article_content_breaks = textwrap.wrap(article_content, width=line_width)

print('Văn bản gốc:')
# Print the content with line breaks
for line in article_content_breaks:
    print(line)
print("\n")

def get_stopwords_list(stop_file_path):
    """load stop words """

    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return list(frozenset(stop_set))


def _create_dictionary_table(text_string) -> dict:
    # Chỉnh đường dẫn này stopword
    stopwords_path = "/app/vietnamese-stopwords.txt"
    stopwords = get_stopwords_list(stopwords_path)
    #print(stopwords)
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
        sentence_wordcount = (len(word_tokenize(sentence)))
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
    sum_values = 0
    for entry in sentence_weight:
        sum_values += sentence_weight[entry]

    # getting sentence average value from source text
    average_score = (sum_values / len(sentence_weight))

    return average_score


def _get_article_summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    article_summary = ''

    for sentence in sentences:
        if sentence[:7] in sentence_weight and sentence_weight[sentence[:7]] >= (threshold):
            article_summary += " " + sentence
            sentence_counter += 1

    return article_summary


def _run_article_summary(article):
    # creating a dictionary for the word frequency table
    frequency_table = _create_dictionary_table(article)

    # tokenizing the sentences
    sentences = sent_tokenize(article)

    # algorithm for scoring a sentence by its words
    sentence_scores = _calculate_sentence_scores(sentences, frequency_table)

    # getting the threshold
    threshold = _calculate_average_score(sentence_scores)

    # producing the summary
    article_summary = _get_article_summary(sentences, sentence_scores, 1 * threshold)

    return article_summary


if __name__ == '__main__':
    summary_results = _run_article_summary(article_content)

    # Wrap the content into multiple lines
    summary_results_breaks = textwrap.wrap(summary_results, width=line_width)

    print('\nVăn bản tóm tắt:')
    # Print the content with line breaks
    for line in summary_results_breaks:
        print(line)
