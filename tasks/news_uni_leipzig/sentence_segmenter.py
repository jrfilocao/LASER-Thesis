#!/usr/bin/python3

import argparse
import re
import syntok.segmenter as segmenter
from article_parse import find_articles
from encoding_resolver import fix_text_encoding
from file_writer import write_id_sentence_pair_to_file, write_sentence_id_to_file, write_sentence_to_file
from language_identification import is_sentence_language_not_correct

SENTENCE_WORD_COUNT_MINIMUM = 10
OUTPUT_DIRECTORY = './output_files/'


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Finding articles for all languages in crawled news texts')
    parser.add_argument('--input-file-name', required=True,
                        help='input file name of news articles in a specific language')
    parser.add_argument('--line-count', type=int, required=True,
                        help='minimum count of consecutive lines to form an article')
    parser.add_argument('--average-line-word-count', type=int, required=True,
                        help='minimum average word count in a line to form an article')
    parser.add_argument('--language', required=True,
                        help='language of the news articles')
    return parser


def _get_id_sentence_output_file_name(language):
    return OUTPUT_DIRECTORY + language + '_id_sentence_pairs'


def _get_ids_output_file_name(language):
    return OUTPUT_DIRECTORY + language + '_ids'


def _get_sentences_output_file_name(language):
    return OUTPUT_DIRECTORY + language + '_sentences'


def _get_article_elements_as_text(article):
    return ''.join(article);


def _remove_all_quote_signs(text):
    return text.replace('“', '').replace('„', '').replace('"', '');


def _set_new_line_in_the_middle_to_dot(text):
    return re.sub(r'(\S\s*)\n(\s*\S*)', r'\1. \2', text)


def _remove_invalid_characters(text):
    text_without_quote_signs = _remove_all_quote_signs(text)
    return _set_new_line_in_the_middle_to_dot(text_without_quote_signs)


def _segment_text_into_sentences(article: str):
    sentences = []
    for paragraph in segmenter.process(article):
        for sentence in paragraph:
            sentences.append("".join(map(str, sentence)).lstrip())
    return sentences


def _write_valid_sentence_information_to_files(id_sentence_pair_file,
                                               ids_file,
                                               sentences_file,
                                               article_index,
                                               sentence_index,
                                               sentence,
                                               input_file_name):
    write_id_sentence_pair_to_file(id_sentence_pair_file, article_index, sentence, sentence_index, input_file_name)
    write_sentence_id_to_file(ids_file, article_index, sentence_index, input_file_name)
    write_sentence_to_file(sentences_file, sentence)


def _has_not_minimum_word_count(sentence):
    return len(sentence.strip().split()) < SENTENCE_WORD_COUNT_MINIMUM


if __name__ == "__main__":
    parser = _get_argument_parser()
    arguments = parser.parse_args()
    articles = find_articles(arguments.input_file_name, arguments.line_count, arguments.average_line_word_count)

    with open(_get_id_sentence_output_file_name(arguments.language), 'a') as id_sentence_pairs_file, \
         open(_get_ids_output_file_name(arguments.language), 'a') as ids_file,\
         open(_get_sentences_output_file_name(arguments.language), 'a') as sentences_file:

        valid_sentences = 0
        for article_index, article in enumerate(articles, start=1):
            article_text = _get_article_elements_as_text(article)
            right_encoded_article_text = fix_text_encoding(article_text)
            sanitized_article_text = _remove_invalid_characters(right_encoded_article_text)
            article_sentences = _segment_text_into_sentences(sanitized_article_text)

            for sentence_index, sentence in enumerate(article_sentences, start=1):
                if _has_not_minimum_word_count(sentence):
                    break

                if is_sentence_language_not_correct(sentence, arguments.language):
                    break

                valid_sentences += 1

                _write_valid_sentence_information_to_files(id_sentence_pairs_file,
                                                           ids_file,
                                                           sentences_file,
                                                           article_index,
                                                           sentence_index,
                                                           sentence,
                                                           arguments.input_file_name)
        print('valid_sentences', valid_sentences, 'input_file_name', arguments.input_file_name)
