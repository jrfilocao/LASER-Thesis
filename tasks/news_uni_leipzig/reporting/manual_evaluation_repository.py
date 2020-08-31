#!/usr/bin/python3

import psycopg2


SELECT_ARTICLE_PAIRS_AND = """
select source_article_id, target_article_id
from matched_article
where source_language = %s and target_language = %s
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_ARTICLE_PAIRS_OR = """
select source_article_id, target_article_id
from matched_article
where source_language = %s and target_language = %s
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_ARTICLE_PAIRS_ONLY = """
select source_article_id, target_article_id
from matched_article
where source_language = %s and target_language = %s
and named_entities_score is not null
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_FALSE_POSITIVE_ARTICLE_PAIRS_AND = """
select source_article_id, target_article_id
from matched_article
where source_language = %s and target_language = %s
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
and substring(source_article_id, 0, 58) != substring(target_article_id, 0, 58)
group by matched_article.source_article_id, matched_article.target_article_id
"""

SELECT_FALSE_POSITIVE_ARTICLE_PAIRS_OR = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
and substring(source_article_id, 0, 58) != substring(target_article_id, 0, 58)
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_FALSE_POSITIVE_ARTICLE_PAIRS_ONLY = """
select source_article_id, target_article_id
from matched_article
where source_language = %s and target_language = %s
and named_entities_score is not null
and sentence_candidates_score >= 1.05
and substring(source_article_id, 0, 58) != substring(target_article_id, 0, 58)
group by matched_article.source_article_id, matched_article.target_article_id;
"""


SELECT_MATCHED_SENTENCES_BY_ARTICLE_IDS = """
select source_sentence, target_sentence
from matched_article
where source_article_id = %s
and target_article_id = %s;
"""

SELECT_NAMED_ENTITIES_FROM_ARTICLE_PAIR = """
select named_entities_score
from matched_article
where source_article_id = %s
and target_article_id = %s
limit 1;
"""


def get_article_pairs_and(source_language, target_language, database_cursor):
    try:
        database_cursor.execute(SELECT_ARTICLE_PAIRS_AND, (source_language, target_language))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_positive_article_pairs_and(source_language, target_language, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_POSITIVE_ARTICLE_PAIRS_AND, (source_language, target_language))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_positive_article_pairs_only(source_language, target_language, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_POSITIVE_ARTICLE_PAIRS_ONLY, (source_language, target_language))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_positive_article_pairs_or(source_language, target_language, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_POSITIVE_ARTICLE_PAIRS_OR, (source_language, target_language))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_matched_sentence_pairs_by_article_ids(source_article_id, target_article_id, database_cursor):
    try:
        database_cursor.execute(SELECT_MATCHED_SENTENCES_BY_ARTICLE_IDS, (source_article_id, target_article_id))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_named_entities_by_article_ids(source_article_id, target_article_id, database_cursor):
    try:
        database_cursor.execute(SELECT_NAMED_ENTITIES_FROM_ARTICLE_PAIR, (source_article_id, target_article_id))
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

