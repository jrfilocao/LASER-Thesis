#!/usr/bin/python3

import psycopg2


SELECT_TRIPLE_SIMILAR_ARTICLES_SQL = """
WITH en_de_sentences AS
(
select distinct source_sentence, target_sentence
from matched_article
where named_entities_score is not null
and sentence_candidates_score > 1.025
and number_of_similar_sentences > 1
and source_language = 'en'
and target_language = 'de'
),
de_pt_sentences AS
(
select distinct source_sentence, target_sentence
from matched_article
where named_entities_score is not null
and sentence_candidates_score > 1.025
and number_of_similar_sentences > 1
and source_language = 'de'
and target_language = 'pt'
),
en_pt_sentences AS
(
select distinct source_sentence, target_sentence
from matched_article
where named_entities_score is not null
and sentence_candidates_score > 1.025
and number_of_similar_sentences > 1
and source_language = 'en'
and target_language = 'pt'
),
triple_sentences AS
(
SELECT
en_de.source_sentence en,
de_pt.target_sentence pt,
en_de.target_sentence de
FROM en_de_sentences en_de
INNER JOIN de_pt_sentences de_pt ON (en_de.target_sentence = de_pt.source_sentence)
UNION ALL
SELECT
en_pt.source_sentence en,
en_pt.target_sentence pt,
de_pt.source_sentence de
FROM en_pt_sentences en_pt
INNER JOIN de_pt_sentences de_pt ON (en_pt.target_sentence = de_pt.target_sentence)
UNION ALL
SELECT distinct
en_pt.source_sentence en,
en_pt.target_sentence pt,
en_de.target_sentence de
FROM en_pt_sentences en_pt
INNER JOIN en_de_sentences en_de ON (en_pt.source_sentence = en_de.source_sentence)
)
SELECT DISTINCT en, pt, de
FROM triple_sentences;
"""

SELECT_ARTICLE_SENTENCES_BY_SENTENCE = """
WITH article_id_from_sentence AS
(
SELECT article_id 
FROM sentence 
WHERE sentence = %s
LIMIT 1
)
SELECT sentence 
FROM sentence 
WHERE article_id IN (SELECT article_id FROM article_id_from_sentence);
"""


def get_triple_similar_article_sentences(database_cursor):
    try:
        database_cursor.execute(SELECT_TRIPLE_SIMILAR_ARTICLES_SQL, ())
        all_article_tuples = database_cursor.fetchall()
        return all_article_tuples
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_sentences_from_first_article_found(sentence, database_cursor):
    try:
        database_cursor.execute(SELECT_ARTICLE_SENTENCES_BY_SENTENCE, (sentence,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)