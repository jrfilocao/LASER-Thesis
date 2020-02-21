#!/usr/bin/python3

import psycopg2


SELECT_TOTAL_SENTENCE_PAIRS = """select count(*) from matched_article;"""

SELECT_UNIQUE_ARTICLE_PAIRS = """
select source_article_id, target_article_id
from matched_article
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES = """
select source_article_id, target_article_id
from matched_article
where named_entities_score is not null
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES = """
select source_article_id, target_article_id
from matched_article
where named_entities_score is not null
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_MORE_THAN_2_SENTENCES = """
select source_article_id, target_article_id
from matched_article
where number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITHOUT_COMMON_NAMED_ENTITIES_AND_WITH_MORE_THAN_2_SENTENCE = """
select source_article_id, target_article_id
from matched_article
where named_entities_score is null
and number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_EN_DE = """
select count(*)
from matched_article
where source_language = 'en' and target_language = 'de';
"""

SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_EN_PT = """
select count(*)
from matched_article
where source_language = 'en' and target_language = 'pt';
"""

SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_DE_PT = """
select count(*)
from matched_article
where source_language = 'de' and target_language = 'pt';
"""

SELECT_UNIQUE_ARTICLE_PAIRS_EN_DE = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_EN_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_DE_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_DE = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and named_entities_score is not null
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_DE_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and named_entities_score is not null
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_EN_DE = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_EN_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_DE_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_DE = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and named_entities_score is not null
and number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_DE_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and named_entities_score is not null
and number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id;
"""


def get_total_sentence_pairs_count(database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_SENTENCE_PAIRS, ())
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_unique_article_pairs_count(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_unique_article_pairs_with_common_named_entities(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_unique_article_pairs_with_more_than_2_sentences(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_MORE_THAN_2_SENTENCES, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITHOUT_COMMON_NAMED_ENTITIES_AND_WITH_MORE_THAN_2_SENTENCE, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_potential_similar_sentences_en_de(database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_EN_DE, ())
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_potential_similar_sentences_en_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_EN_PT, ())
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_potential_similar_sentences_de_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_DE_PT, ())
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_en_de(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_EN_DE, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_en_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_EN_PT, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_de_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_DE_PT, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_with_common_named_entities_en_de(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_DE, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_with_common_named_entities_en_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_PT, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_with_common_named_entities_de_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_DE_PT, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_more_than_2_sentences_en_de(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_EN_DE, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_more_than_2_sentences_en_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_EN_PT, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_more_than_2_sentences_de_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_DE_PT, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_DE, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_PT, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt(database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_DE_PT, ())
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)