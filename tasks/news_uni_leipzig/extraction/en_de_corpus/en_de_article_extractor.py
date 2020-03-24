#!/usr/bin/python3


import os
from os import listdir
from os.path import isfile, join
import sys
assert os.environ.get('NEWS_TASK'), 'Please set the environment variable NEWS_TASK'

NEWS_TASK = os.environ['NEWS_TASK']
sys.path.append(NEWS_TASK + '/extraction')
sys.path.append(NEWS_TASK + '/extraction/en_de_corpus')

import re
import syntok.segmenter as segmenter

from en_de_article_id_sentence_extractor import extract_articles_from_file
from id_sentence_writer import write_id_sentence_pair_to_file, write_sentence_to_file
from language_identification import is_sentence_language_not_correct

INPUT_DIRECTORY = NEWS_TASK + '/input_files/'
OUTPUT_DIRECTORY = NEWS_TASK + '/output_files/'

FINDING_LANGUAGE_IN_FILE_NAME_REGEX = 'de-news-\d{4}-\d{2}-\d{2}.(\w{2}).al'


def _get_file_lines(input_file):
    return input_file.readlines()


def _get_language(input_file_name):
    matches = re.search(FINDING_LANGUAGE_IN_FILE_NAME_REGEX, input_file_name)
    return matches.group(1)


def _get_id_sentence_output_file_name(language):
    return OUTPUT_DIRECTORY + language + '_id_sentence_pairs'


def _get_sentences_output_file_name(language):
    return OUTPUT_DIRECTORY + language + '_sentences'


def _write_id_sentence_pair_to_file(output_file, article_id, sentence, sentence_index):
    sentence_id = _get_sentence_id(article_id, sentence_index)
    id_sentence_pair = _get_id_sentence_pair(sentence, sentence_id)
    output_file.write(id_sentence_pair)


def _write_sentence_to_file(output_file, sentence):
    sentence_line = _get_sentence_line(sentence)
    output_file.write(sentence_line)


def _get_sentence_id(article_id, sentence_index):
    return article_id + '_sentence_' + str(sentence_index)


def _get_id_sentence_pair(sentence, sentence_id):
    return sentence_id + '    ' + sentence + '\n'


def _get_sentence_line(sentence):
    return sentence + '\n'


def _segment_text_into_sentences(raw_sentence: str):
    sentences = []
    for segmented_sentences in segmenter.process(raw_sentence):
        for sentence in segmented_sentences:
            sentences.append("".join(map(str, sentence)).lstrip())
    return sentences


def _get_segmented_sentences(raw_article_sentences):
    segmented_sentences = []
    for raw_sentence in raw_article_sentences:
        segmented_sentences.extend(_segment_text_into_sentences(raw_sentence))
    return segmented_sentences


if __name__ == "__main__":

    input_file_names = [f for f in listdir(INPUT_DIRECTORY) if isfile(join(INPUT_DIRECTORY, f))]

    number_of_article_tags = 0
    number_of_articles = 0
    number_of_articles_for_iteration = 0
    number_of_empty_articles = 0
    number_of_sentences_in_wrong_language = 0
    number_of_articles_not_computed_due_wrong_language = 0
    for input_file_name in input_file_names:

        language = _get_language(input_file_name)
        articles, article_id_tag_count = extract_articles_from_file(INPUT_DIRECTORY + input_file_name, language)

        number_of_article_tags += article_id_tag_count
        number_of_articles += len(articles)
        with open(_get_id_sentence_output_file_name(language), 'a') as id_sentence_pairs_file, \
             open(_get_sentences_output_file_name(language), 'a') as sentences_file:

            for article_id in articles.keys():
                raw_article_sentences = articles[article_id]
                article_sentences = _get_segmented_sentences(raw_article_sentences)
                number_of_articles_for_iteration += 1
                if len(article_sentences) == 0:
                    number_of_empty_articles += 1
                for sentence_index, sentence in enumerate(article_sentences, start=1):
                    if is_sentence_language_not_correct(sentence, language):
                        print('sentence language not valid')
                        number_of_sentences_in_wrong_language += 1
                        if len(article_sentences) == 1:
                            number_of_articles_not_computed_due_wrong_language += 1
                        continue
                    _write_id_sentence_pair_to_file(id_sentence_pairs_file, article_id, sentence, sentence_index)
                    _write_sentence_to_file(sentences_file, sentence)

        print('number_of_article_tags', number_of_article_tags)
        print('number_of_articles', number_of_articles)
        print('number_of_articles_written', number_of_articles_for_iteration)
        print('number_of_empty_articles', number_of_empty_articles)
        print('number_of_sentence_in_wrong_language', number_of_sentences_in_wrong_language)
        print('number_of_articles_not_computed_due_wrong_language', number_of_articles_not_computed_due_wrong_language)