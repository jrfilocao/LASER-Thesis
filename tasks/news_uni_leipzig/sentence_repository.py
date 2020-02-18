#!/usr/bin/python3

import psycopg2


INSERT_SENTENCE_SQL = """INSERT INTO sentence(sentence_id, article_id, sentence) VALUES(%s, %s, %s);"""

SELECT_ARTICLES_BY_SENTENCE_SQL = """SELECT DISTINCT article_id FROM sentence WHERE sentence = %s;"""

SELECT_SENTENCES_BY_ARTICLE_ID_SQL = """SELECT sentence FROM sentence WHERE article_id = %s;"""


def insert_sentence(sentence_id, article_id, sentence, database_cursor):
    try:
        database_cursor.execute(INSERT_SENTENCE_SQL, (sentence_id, article_id, sentence))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_articles_from_sentence(sentence, database_cursor):
    try:
        database_cursor.execute(SELECT_ARTICLES_BY_SENTENCE_SQL, (sentence,))
        return database_cursor.fetchall()[0][0] # TODO return all items
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_sentences_from_article(article_id, database_cursor):
    try:
        database_cursor.execute(SELECT_SENTENCES_BY_ARTICLE_ID_SQL, (article_id,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)