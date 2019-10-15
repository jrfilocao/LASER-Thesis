#!/usr/bin/python3

import argparse
import re
import syntok.segmenter as segmenter
from finding_articles import find_articles


def _get_argumet_parser():
    parser = argparse.ArgumentParser(description='Finding articles for all languages in crawled news texts')
    parser.add_argument('--input-file-name', required=True,
                        help='input file name of news articles in a specific language')
    parser.add_argument('--line-count', type=int, required=True,
                        help='minimum count of consecutive lines to form an article')
    parser.add_argument('--average-line-word-count', type=int, required=True,
                        help='minimum average word count in a line to form an article')
    return parser


def _get_output_file_name(input_file_name: str):
    return input_file_name + '_id_sentence_list'


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


def _get_sentence_id(base_sentence_id, article_index, sentence_index):
    return base_sentence_id + '_article_' + str(article_index) + '_sentence_' + str(sentence_index)


def _get_id_sentence_pair(sentence, sentence_id):
    return sentence_id + '    ' + sentence + '\n'


def _write_article_sentences_into_file(output_file_name, base_sentence_id, article_index, sentences):
    with open(output_file_name, 'a') as output_file:
        for sentence_index, sentence in enumerate(sentences, start=1):
            sentence_id = _get_sentence_id(base_sentence_id, article_index, sentence_index)
            id_sentence_pair = _get_id_sentence_pair(sentence, sentence_id)
            output_file.write(id_sentence_pair)


if __name__ == "__main__":
    parser = _get_argumet_parser()
    arguments = parser.parse_args()
    output_file_name = _get_output_file_name(arguments.input_file_name)
    articles = find_articles(arguments.input_file_name, arguments.line_count, arguments.average_line_word_count)

    for article_index, article in enumerate(articles, start=1):
        article_text = _get_article_elements_as_text(article)
        clean_article_text = _remove_invalid_characters(article_text)
        article_sentences = _segment_text_into_sentences(clean_article_text)
        base_sentence_id = arguments.input_file_name
        _write_article_sentences_into_file(output_file_name, base_sentence_id, article_index, article_sentences)
