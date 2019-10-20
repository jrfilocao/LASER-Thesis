#!/usr/bin/python3

import argparse
import re
import syntok.segmenter as segmenter
from finding_articles import find_articles
from fixing_text_encoding import fix_text_encoding
from writing_to_file import write_id_sentence_pair_to_file, write_sentence_id_to_file, write_sentence_to_file


def _get_argumet_parser():
    parser = argparse.ArgumentParser(description='Finding articles for all languages in crawled news texts')
    parser.add_argument('--input-file-name', required=True,
                        help='input file name of news articles in a specific language')
    parser.add_argument('--line-count', type=int, required=True,
                        help='minimum count of consecutive lines to form an article')
    parser.add_argument('--average-line-word-count', type=int, required=True,
                        help='minimum average word count in a line to form an article')
    return parser


def _get_article_elements_as_text(article):
    return ''.join(article);


def _remove_all_quote_signs(text):
    return text.replace('“', '').replace('„', '').replace('"', '');


def _set_new_line_in_the_middle_to_dot(text):
    return re.sub(r'(\w+\s*)\n(\s*\w+)', r'\1. \2', text)


def _remove_invalid_characters(text):
    text_without_quote_signs = _remove_all_quote_signs(text)
    return _set_new_line_in_the_middle_to_dot(text_without_quote_signs)


def _segment_text_into_sentences(article: str):
    sentences = []
    for paragraph in segmenter.process(article):
        for sentence in paragraph:
            sentences.append("".join(map(str, sentence)).lstrip())
    return sentences


if __name__ == "__main__":
    parser = _get_argumet_parser()
    arguments = parser.parse_args()
    articles = find_articles(arguments.input_file_name, arguments.line_count, arguments.average_line_word_count)

    for article_index, article in enumerate(articles, start=1):
        article_text = _get_article_elements_as_text(article)
        right_encoded_article_text = fix_text_encoding(article_text)
        sanitized_article_text = _remove_invalid_characters(right_encoded_article_text)
        article_sentences = _segment_text_into_sentences(sanitized_article_text)

        for sentence_index, sentence in enumerate(article_sentences, start=1):
            write_id_sentence_pair_to_file(arguments.input_file_name, article_index, sentence, sentence_index)
            write_sentence_id_to_file(arguments.input_file_name, article_index, sentence_index)
            write_sentence_to_file(arguments.input_file_name, sentence)