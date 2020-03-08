#!/usr/bin/python3

import psycopg2


SELECT_TRIPLE_SIMILAR_ARTICLES_SQL = """
WITH en_de_sentences AS
(
select distinct source_sentence, target_sentence, source_article_id, target_article_id, named_entities_score, number_of_similar_sentences
from matched_article
where named_entities_score is not null
and sentence_candidates_score > 1
and number_of_similar_sentences > 1
and source_language = 'en'
and target_language = 'de'
),
de_pt_sentences AS
(
select distinct source_sentence, target_sentence, source_article_id, target_article_id, named_entities_score, number_of_similar_sentences
from matched_article
where named_entities_score is not null
and sentence_candidates_score > 1
and number_of_similar_sentences > 1
and source_language = 'de'
and target_language = 'pt'
),
en_pt_sentences AS
(
select distinct source_sentence, target_sentence, source_article_id, target_article_id, named_entities_score, number_of_similar_sentences
from matched_article
where named_entities_score is not null
and sentence_candidates_score > 1
and number_of_similar_sentences > 1
and source_language = 'en'
and target_language = 'pt'
)
SELECT
en_de.source_article_id,
de_pt.target_article_id,
en_de.target_article_id
FROM en_de_sentences en_de
INNER JOIN de_pt_sentences de_pt ON (en_de.target_sentence = de_pt.source_sentence)
UNION ALL
SELECT
en_pt.source_article_id,
en_pt.target_article_id,
de_pt.source_article_id
FROM en_pt_sentences en_pt
INNER JOIN de_pt_sentences de_pt ON (en_pt.target_sentence = de_pt.target_sentence)
UNION ALL
SELECT
en_pt.source_article_id,
en_pt.target_article_id,
en_de.target_article_id
FROM en_pt_sentences en_pt
INNER JOIN en_de_sentences en_de ON (en_pt.source_sentence = en_de.source_sentence);
"""


def get_triple_similar_articles(database_cursor):
    try:
        database_cursor.execute(SELECT_TRIPLE_SIMILAR_ARTICLES_SQL, ())
        all_article_tuples = database_cursor.fetchall()
        return all_article_tuples
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)