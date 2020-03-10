#!/usr/bin/python3

import re

FINDING_LANGUAGE_IN_FILE_NAME_REGEX = 'de-news-\d{4}-\d{2}-\d{2}.(\w{2}).al'

ARTICLE = 'article'
EMPTY_STRING = ''
NEW_LINE = '\n'
UNDERSCORE = '_'
HYPHEN = '-'
CLOSE_BRACKET = '>'
ARTICLE_ID_TAG_BEGIN = '<DOC de-news-'


def extract_articles_from_file(input_file_name):
    with open(input_file_name, 'r') as input_file:

        language = _get_language(input_file_name)

        articles = {}
        article_id = EMPTY_STRING
        article_sentences = []

        file_lines = input_file.readlines()
        for file_line in file_lines:
            if ARTICLE_ID_TAG_BEGIN in file_line:
                if article_sentences:
                    articles[article_id] = article_sentences
                article_sentences = []
                article_id = _get_article_id(file_line, language)
            else:
                article_sentences.append(file_line)
    return articles


def _get_language(input_file_name):
    matches = re.search(FINDING_LANGUAGE_IN_FILE_NAME_REGEX, input_file_name)
    return matches.group(1)


def _get_article_id(file_line, language):
    date_article_number = file_line.replace(ARTICLE_ID_TAG_BEGIN, EMPTY_STRING) \
                                   .replace(CLOSE_BRACKET, EMPTY_STRING) \
                                   .replace(HYPHEN, UNDERSCORE) \
                                   .replace(NEW_LINE, EMPTY_STRING)
    last_underscore_index = date_article_number.rfind(UNDERSCORE)
    return language + UNDERSCORE + date_article_number[:last_underscore_index] + UNDERSCORE + ARTICLE + date_article_number[last_underscore_index:]
