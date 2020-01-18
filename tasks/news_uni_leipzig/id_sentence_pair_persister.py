#!/usr/bin/python3

import argparse
import psycopg2


INSERT_SENTENCE_SQL = """INSERT INTO sentence(sentence_id, article_id, sentence) VALUES(%s, %s, %s);"""


def _get_argument_parser():
    parser = argparse.ArgumentParser(description='Persisting sentences from files in Redis')
    parser.add_argument('--sentence-files', nargs='+', help='sentence files to be processed', required=True)
    return parser


def _get_database_connection():
    return psycopg2.connect(host="database", database="postgres", user="postgres", password="postgres")


def _get_id_sentence(id_sentence_pair):
    id_sentence = id_sentence_pair.split('    ')
    if len(id_sentence) == 2:
        return id_sentence[0].strip(), id_sentence[1].strip()
    raise ValueError


def _get_article_id(sentence_id):
    article_end_index = sentence_id.find('_sentence_')
    return sentence_id[:article_end_index]


def _insert_sentence(sentence_id, article_id, sentence, database_cursor):
    try:
        database_cursor.execute(INSERT_SENTENCE_SQL, (sentence_id, article_id, sentence))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


if __name__ == "__main__":

    parser = _get_argument_parser()
    arguments = parser.parse_args()

    try:
        database_connection = _get_database_connection()
        database_cursor = database_connection.cursor()

        for sentence_file in arguments.sentence_files:
            with open(sentence_file, 'r') as id_sentence_pairs_file:
                id_sentence_pairs = id_sentence_pairs_file.readlines()
                for id_sentence_pair in id_sentence_pairs:
                    try:
                        sentence_id, sentence = _get_id_sentence(id_sentence_pair)
                        article_id = _get_article_id(sentence_id)
                        _insert_sentence(sentence_id, article_id, sentence, database_cursor)
                    except ValueError:
                        pass
            database_connection.commit()

    finally:
        if database_connection is not None:
            database_connection.close()