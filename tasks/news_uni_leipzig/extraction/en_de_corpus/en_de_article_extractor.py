#!/usr/bin/python3

# import re
# import syntok.segmenter as segmenter

# import os
from os import listdir
from os.path import isfile, join
import sys
# assert os.environ.get('NEWS_TASK'), 'Please set the environment variable NEWS_TASK'
#
# NEWS_TASK = os.environ['NEWS_TASK']
# sys.path.append(NEWS_TASK + '/extraction')
#
# from encoding_resolver import fix_text_encoding
# from id_sentence_writer import write_id_sentence_pair_to_file
# from language_identification import is_sentence_language_not_correct

# INPUT_DIRECTORY = NEWS_TASK + '/input_files/'
# OUTPUT_DIRECTORY = NEWS_TASK + '/output_files/'
from IPython.nbconvert.filters import get_lines

from article_parser import extract_articles_from_file

INPUT_DIRECTORY = '../../input_files/'


def _get_file_lines(input_file):
    return input_file.readlines()


if __name__ == "__main__":

    input_file_names = [f for f in listdir(INPUT_DIRECTORY) if isfile(join(INPUT_DIRECTORY, f))]

    for input_file_name in input_file_names:

        articles = extract_articles_from_file(INPUT_DIRECTORY + input_file_name)
        print(articles)

    # with open(_get_id_sentence_output_file_name(arguments.language), 'a') as id_sentence_pairs_file, \
    #      open(_get_sentences_output_file_name(arguments.language), 'a') as sentences_file:
    #
    #     valid_sentences = 0
    #     for article_index, article in enumerate(articles, start=1):
    #         article_text = _get_article_elements_as_text(article)
    #         right_encoded_article_text = fix_text_encoding(article_text)
    #         sanitized_article_text = _remove_invalid_characters(right_encoded_article_text)
    #         article_sentences = _segment_text_into_sentences(sanitized_article_text)
    #
    #         for sentence_index, sentence in enumerate(article_sentences, start=1):
    #             if _has_not_minimum_word_count(sentence):
    #                 break
    #
    #             if is_sentence_language_not_correct(sentence, arguments.language):
    #                 break
    #
    #             valid_sentences += 1
    #
    #             _write_valid_sentence_information_to_files(id_sentence_pairs_file,
    #                                                        ids_file,
    #                                                        sentences_file,
    #                                                        article_index,
    #                                                        sentence_index,
    #                                                        sentence,
    #                                                        arguments.input_file_name)
    #     print('valid_sentences', valid_sentences, 'input_file_name', arguments.input_file_name)
