#!/usr/bin/python3

import argparse
from common.database_connector import get_database_connection
from similarity.sentence_repository import insert_sentence


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Persisting id sentence pairs from files in the database')
    parser.add_argument('--id-sentence-pair-files', nargs='+', help='id sentence pair files to be processed', required=True)
    return parser


def _get_id_sentence(id_sentence_pair):
    id_sentence = id_sentence_pair.split('    ')
    if len(id_sentence) == 2:
        return id_sentence[0].strip(), id_sentence[1].strip()
    raise ValueError


def _get_article_id(sentence_id):
    article_end_index = sentence_id.find('_sentence_')
    return sentence_id[:article_end_index]


def validate_sentence_length(sentence):
    if len(sentence) > 5000:
        raise ValueError


if __name__ == "__main__":

    parser = _get_argument_parser()
    arguments = parser.parse_args()

    try:
        database_connection = get_database_connection()
        database_cursor = database_connection.cursor()

        for sentence_file in arguments.id_sentence_pair_files:
            with open(sentence_file, 'r') as id_sentence_pairs_file:
                id_sentence_pairs = id_sentence_pairs_file.readlines()
                for id_sentence_pair in id_sentence_pairs:
                    try:
                        sentence_id, sentence = _get_id_sentence(id_sentence_pair)
                        article_id = _get_article_id(sentence_id)
                        validate_sentence_length(sentence)
                        insert_sentence(sentence_id, article_id, sentence, database_cursor)
                    except ValueError:
                        continue
            database_connection.commit()

    finally:
        if database_connection is not None:
            database_connection.close()