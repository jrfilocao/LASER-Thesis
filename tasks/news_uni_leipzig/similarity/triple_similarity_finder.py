#!/usr/bin/python3


import argparse
import os
import sys
assert os.environ.get('NEWS_TASK'), 'Please set the environment variable NEWS_TASK'
NEWS_TASK = os.environ['NEWS_TASK']
sys.path.append(NEWS_TASK + '/common')
sys.path.append(NEWS_TASK + '/similarity')

from database_connector import get_database_connection
from triple_similarity_repository import *


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Get similar articles in all three languages')
    parser.add_argument('--output-base-file-name', default='./output_files/triple_similar_articles',
                        help='output base file name')
    return parser


def _get_article_sentences_as_text(sentences):
    return "\n".join(sentence_tuple[0] for sentence_tuple in sentences)


def _get_output_file_name(output_base_file_name, language):
    return output_base_file_name + '_' + language + '.txt'


def _get_output_article_id(triple_article_index):
    return 'article-' + str(triple_article_index) + '\n'


def _get_triple_article_tuple(output_article_id,
                              en_article_sentence,
                              pt_article_sentence,
                              de_article_sentence,
                              en_article_sentences_text,
                              pt_article_sentences_text,
                              de_article_sentences_text):
    return (output_article_id,
            [en_article_sentence],
            [pt_article_sentence],
            [de_article_sentence],
            en_article_sentences_text,
            pt_article_sentences_text,
            de_article_sentences_text)


def _add_triple_sentences_into_articles_if_present(en_article_sentence, pt_article_sentence, de_article_sentence, triple_articles):
    for triple_article in triple_articles:
        if en_article_sentence in triple_article[4] or pt_article_sentence in triple_article[5] or de_article_sentence in triple_article[6]:
            triple_article[1].append(en_article_sentence)
            triple_article[2].append(pt_article_sentence)
            triple_article[3].append(de_article_sentence)
            return True
    return False


def _get_triple_article(en_article_sentence, pt_article_sentence, de_article_sentence, triple_article_index):
    en_article_sentences = get_sentences_from_first_article_found(en_article_sentence, database_cursor)
    pt_article_sentences = get_sentences_from_first_article_found(pt_article_sentence, database_cursor)
    de_article_sentences = get_sentences_from_first_article_found(de_article_sentence, database_cursor)
    en_article_sentences_text = _get_article_sentences_as_text(en_article_sentences)
    pt_article_sentences_text = _get_article_sentences_as_text(pt_article_sentences)
    de_article_sentences_text = _get_article_sentences_as_text(de_article_sentences)
    output_article_id = _get_output_article_id(triple_article_index)
    return _get_triple_article_tuple(output_article_id,
                                     en_article_sentence,
                                     pt_article_sentence,
                                     de_article_sentence,
                                     en_article_sentences_text,
                                     pt_article_sentences_text,
                                     de_article_sentences_text)


def _write_triple_articles(triple_articles, en_output_file, pt_output_file, de_output_file):
    for triple_article in triple_articles:
        article_id = triple_article[0]
        en_output_file.write(article_id)
        pt_output_file.write(article_id)
        de_output_file.write(article_id)

        en_output_file.write('-------\n')
        pt_output_file.write('-------\n')
        de_output_file.write('-------\n')

        en_article_sentences_text = triple_article[4]
        pt_article_sentences_text = triple_article[5]
        de_article_sentences_text = triple_article[6]

        en_output_file.write(en_article_sentences_text)
        pt_output_file.write(pt_article_sentences_text)
        de_output_file.write(de_article_sentences_text)

        en_output_file.write('\n\n')
        pt_output_file.write('\n\n')
        de_output_file.write('\n\n')
        en_output_file.write('-------\n')
        pt_output_file.write('-------\n')
        de_output_file.write('-------\n')

        en_article_sentences = triple_article[1]
        pt_article_sentences = triple_article[2]
        de_article_sentences = triple_article[3]

        for en_article_sentence in en_article_sentences:
            en_output_file.write(en_article_sentence + '\n')
            en_output_file.write('-------\n')
        for pt_article_sentence in pt_article_sentences:
            pt_output_file.write(pt_article_sentence + '\n')
            pt_output_file.write('-------\n')
        for de_article_sentence in de_article_sentences:
            de_output_file.write(de_article_sentence + '\n')
            de_output_file.write('-------\n')

        en_output_file.write('\n\n\n')
        pt_output_file.write('\n\n\n')
        de_output_file.write('\n\n\n')


def _get_triple_articles(triple_article_sentences):
    triple_articles = []
    triple_article_index = 1
    for triple_article_sentence in triple_article_sentences:
        sentences_added_in_previous_articles = _add_triple_sentences_into_articles_if_present(triple_article_sentence[0],
                                                                                              triple_article_sentence[1],
                                                                                              triple_article_sentence[2],
                                                                                              triple_articles)

        if not sentences_added_in_previous_articles:
            triple_article_tuple = _get_triple_article(triple_article_sentence[0], triple_article_sentence[1], triple_article_sentence[2], triple_article_index)
            triple_articles.append(triple_article_tuple)
            triple_article_index += 1

    return triple_articles


if __name__ == "__main__":
    parser = _get_argument_parser()
    arguments = parser.parse_args()

    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        de_output_file_name = _get_output_file_name(arguments.output_base_file_name, 'de')
        pt_output_file_name = _get_output_file_name(arguments.output_base_file_name, 'pt')
        en_output_file_name = _get_output_file_name(arguments.output_base_file_name, 'en')

        with open(de_output_file_name, 'w') as de_output_file, \
             open(pt_output_file_name, 'w') as pt_output_file, \
             open(en_output_file_name, 'w') as en_output_file:

            triple_article_sentences = get_triple_similar_article_sentences(database_cursor)
            triple_articles = _get_triple_articles(triple_article_sentences)
            _write_triple_articles(triple_articles, en_output_file, pt_output_file, de_output_file)

    finally:
        if database_connection is not None:
            database_connection.close()