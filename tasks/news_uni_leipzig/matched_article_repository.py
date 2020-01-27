#!/usr/bin/python3

import psycopg2


INSERT_MATCHED_ARTICLE_SQL = """INSERT INTO matched_article(source_article_id,
                                                            target_article_id,
                                                            source_sentence,
                                                            target_sentence,
                                                            source_article_text,
                                                            target_article_text,
                                                            source_language,
                                                            target_language,
                                                            source_article_url,
                                                            target_article_url,
                                                            named_entities_score,
                                                            number_of_similar_sentences) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

UPDATE_NUMBER_OF_SIMILAR_SENTENCES_SQL = """UPDATE matched_article SET number_of_similar_sentences = %s WHERE source_article_id = %s AND target_article_id = %s;"""


def insert_matched_article(source_article_id,
                           target_article_id,
                           source_sentence,
                           target_sentence,
                           source_article_text,
                           target_article_text,
                           source_language,
                           target_language,
                           source_article_url,
                           target_article_url,
                           named_entities_score,
                           database_cursor):

    try:
        database_cursor.execute(INSERT_MATCHED_ARTICLE_SQL, (source_article_id,
                                                             target_article_id,
                                                             source_sentence,
                                                             target_sentence,
                                                             source_article_text,
                                                             target_article_text,
                                                             source_language,
                                                             target_language,
                                                             source_article_url,
                                                             target_article_url,
                                                             named_entities_score,
                                                             1))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def update_all_number_of_similar_sentences(numbers_of_similar_sentences, database_cursor):
    try:
        for number_of_similar_sentences in numbers_of_similar_sentences:
            database_cursor.execute(UPDATE_NUMBER_OF_SIMILAR_SENTENCES_SQL,
                                    (numbers_of_similar_sentences[number_of_similar_sentences],
                                     number_of_similar_sentences[0],
                                     number_of_similar_sentences[1]))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
