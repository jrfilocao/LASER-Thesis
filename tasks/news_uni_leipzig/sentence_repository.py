#!/usr/bin/python3

import psycopg2


INSERT_SENTENCE_SQL = """INSERT INTO sentence(sentence_id, article_id, sentence) VALUES(%s, %s, %s);"""


def insert_sentence(sentence_id, article_id, sentence, database_cursor):
    try:
        database_cursor.execute(INSERT_SENTENCE_SQL, (sentence_id, article_id, sentence))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)