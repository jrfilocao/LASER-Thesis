#!/usr/bin/python3

import psycopg2


UPDATE_WRONG_SENTENCE_COUNT_BY_ARTICLE_PAIR = """
WITH sentence_count_by_article_pair AS
(
SELECT source_article_id, target_article_id, count(*) as sentence_counter
FROM matched_article 
WHERE source_language = 'en' and target_language = 'pt'
GROUP BY source_article_id, target_article_id
)
UPDATE matched_article
SET number_of_similar_sentences = subquery.sentence_counter
FROM (
SELECT source_article_id, target_article_id, sentence_counter
FROM sentence_count_by_article_pair
) AS subquery
WHERE matched_article.source_article_id = subquery.source_article_id
AND matched_article.target_article_id = subquery.target_article_id
AND subquery.sentence_counter != matched_article.number_of_similar_sentences;
"""


DRY_RUN_UPDATE_WRONG_SENTENCE_COUNT_BY_ARTICLE_PAIR = """
WITH sentence_count_by_article_pair AS
(
SELECT source_article_id, target_article_id, count(*) as sentence_counter
FROM matched_article 
WHERE source_language = 'en' and target_language = 'pt'
GROUP BY source_article_id, target_article_id
)
SELECT count(*)
FROM (
SELECT source_article_id, target_article_id, sentence_counter
FROM sentence_count_by_article_pair
) AS subquery
INNER JOIN matched_article
ON subquery.source_article_id = matched_article.source_article_id
AND subquery.target_article_id = matched_article.target_article_id
WHERE subquery.sentence_counter != matched_article.number_of_similar_sentences;
"""


def get_sentence_count_and_article_pair_tuples(database_cursor):
    try:
        database_cursor.execute(UPDATE_WRONG_SENTENCE_COUNT_BY_ARTICLE_PAIR, ())
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
