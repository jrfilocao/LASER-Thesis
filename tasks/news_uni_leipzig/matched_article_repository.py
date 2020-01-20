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
                                                            named_entities_score) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""


def insert_matched_article(source_article_id,
                           target_article_id,
                           source_sentence,
                           target_sentence,
                           source_article_text,
                           target_article_text,
                           source_language,
                           target_language,
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
                                                             named_entities_score))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)