#!/usr/bin/python3

import psycopg2


SELECT_TOTAL_SENTENCE_PAIRS = """select count(*) from matched_article where sentence_candidates_score >= %s;"""

SELECT_UNIQUE_ARTICLE_PAIRS = """
select source_article_id, target_article_id
from matched_article
where sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES = """
select source_article_id, target_article_id
from matched_article
where named_entities_score is not null
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES = """
select source_article_id, target_article_id
from matched_article
where named_entities_score is not null
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_MORE_THAN_2_SENTENCES = """
select source_article_id, target_article_id
from matched_article
where number_of_similar_sentences > 1
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITHOUT_COMMON_NAMED_ENTITIES_AND_WITH_MORE_THAN_2_SENTENCE = """
select source_article_id, target_article_id
from matched_article
where named_entities_score is null
and number_of_similar_sentences > 1
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

#TODO wiederholte sentences
SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_EN_DE = """
select count(*)
from matched_article
where source_language = 'en' and target_language = 'de'
and sentence_candidates_score >= %s;
"""

SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_EN_PT = """
select count(*)
from matched_article
where source_language = 'en' and target_language = 'pt'
and sentence_candidates_score >= %s;
"""

SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_DE_PT = """
select count(*)
from matched_article
where source_language = 'de' and target_language = 'pt'
and sentence_candidates_score >= %s;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_EN_DE = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_EN_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_DE_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_EN_DE = """
WITH ner_correct_article_pairs AS
(
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and sentence_candidates_score >= %s
and substring(source_article_id, 3) = substring(target_article_id, 3)
group by source_article_id, target_article_id, number_of_similar_sentences
),
all_english_article_ids AS
(
select article_id from sentence where substring(article_id, 0, 3) = 'en'
),
false_negatives_en_articles AS (
select article_id from all_english_article_ids
except
select source_article_id as article_id from ner_correct_article_pairs
)
select article_id as source_article_id, 'de' || substring(article_id, 3) as target_article_id from false_negatives_en_articles;
"""

SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_EN_PT = """
WITH ner_correct_article_pairs AS
(
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'pt'
and named_entities_score is not null
and sentence_candidates_score >= %s
and substring(source_article_id, 3) = substring(target_article_id, 3)
group by source_article_id, target_article_id, number_of_similar_sentences
),
all_english_article_ids AS
(
select article_id from sentence where substring(article_id, 0, 3) = 'en'
),
false_negatives_en_articles AS (
select article_id from all_english_article_ids
except
select source_article_id as article_id from ner_correct_article_pairs
)
select article_id as source_article_id, 'pt' || substring(article_id, 3) as target_article_id from false_negatives_en_articles;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_DE = """
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id, matched_article.number_of_similar_sentences;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_PT = """
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'pt'
and named_entities_score is not null
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id, matched_article.number_of_similar_sentences;
"""

SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_DE_PT = """
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'de' and target_language = 'pt'
and named_entities_score is not null
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id, matched_article.number_of_similar_sentences;
"""

SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_EN_DE = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and number_of_similar_sentences > 1
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_EN_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and number_of_similar_sentences > 1
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_DE_PT = """
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and number_of_similar_sentences > 1
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id;
"""

SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_DE = """
WITH ner_multiple_correct_article_pairs AS
(
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and sentence_candidates_score >= %s
and number_of_similar_sentences > 1
group by source_article_id, target_article_id, number_of_similar_sentences
),
all_english_article_ids AS
(
select article_id from sentence where substring(article_id, 0, 3) = 'en'
),
false_negatives_en_articles AS (
select article_id from all_english_article_ids
except
select source_article_id as article_id from ner_multiple_correct_article_pairs
)
select article_id as source_article_id, 'de' || substring(article_id, 3) as target_article_id from false_negatives_en_articles;
"""

SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_PT = """
WITH ner_multiple_correct_article_pairs AS
(
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'pt'
and named_entities_score is not null
and sentence_candidates_score >= %s
and number_of_similar_sentences > 1
group by source_article_id, target_article_id, number_of_similar_sentences
),
all_english_article_ids AS
(
select article_id from sentence where substring(article_id, 0, 3) = 'en'
),
false_negatives_en_articles AS (
select article_id from all_english_article_ids
except
select source_article_id as article_id from ner_multiple_correct_article_pairs
)
select article_id as source_article_id, 'pt' || substring(article_id, 3) as target_article_id from false_negatives_en_articles;
"""

SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_DE = """
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and sentence_candidates_score >= %s
and number_of_similar_sentences > 1
group by matched_article.source_article_id, matched_article.target_article_id, matched_article.number_of_similar_sentences;
"""

SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_OR_MULTIPLE_SIMILAR_SENTENCES_EN_DE = """
WITH ner_multiple_correct_article_pairs AS
(
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'de'
and sentence_candidates_score >= %s
and (named_entities_score is not null or number_of_similar_sentences > 1)
group by source_article_id, target_article_id, number_of_similar_sentences
),
all_english_article_ids AS
(
select article_id from sentence where substring(article_id, 0, 3) = 'en'
),
false_negatives_en_articles AS (
select article_id from all_english_article_ids
except
select source_article_id as article_id from ner_multiple_correct_article_pairs
)
select article_id as source_article_id, 'de' || substring(article_id, 3) as target_article_id from false_negatives_en_articles;
"""

SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_OR_MULTIPLE_SIMILAR_SENTENCES_EN_PT = """
WITH ner_multiple_correct_article_pairs AS
(
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'pt'
and sentence_candidates_score >= %s
and (named_entities_score is not null or number_of_similar_sentences > 1)
group by source_article_id, target_article_id, number_of_similar_sentences
),
all_english_article_ids AS
(
select article_id from sentence where substring(article_id, 0, 3) = 'en'
),
false_negatives_en_articles AS (
select article_id from all_english_article_ids
except
select source_article_id as article_id from ner_multiple_correct_article_pairs
)
select article_id as source_article_id, 'pt' || substring(article_id, 3) as target_article_id from false_negatives_en_articles;
"""

SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_OR_MULTIPLE_SIMILAR_SENTENCES_EN_DE = """
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'de'
and sentence_candidates_score >= %s
and (named_entities_score is not null or number_of_similar_sentences > 1)
group by matched_article.source_article_id, matched_article.target_article_id, matched_article.number_of_similar_sentences;
"""

SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_OR_MULTIPLE_SIMILAR_SENTENCES_EN_PT = """
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'pt'
and sentence_candidates_score >= %s
and (named_entities_score is not null or number_of_similar_sentences > 1)
group by matched_article.source_article_id, matched_article.target_article_id, matched_article.number_of_similar_sentences;
"""

SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_PT = """
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'en' and target_language = 'pt'
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id, matched_article.number_of_similar_sentences;
"""

SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_DE_PT = """
select source_article_id, target_article_id, number_of_similar_sentences
from matched_article
where source_language = 'de' and target_language = 'pt'
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= %s
group by matched_article.source_article_id, matched_article.target_article_id, matched_article.number_of_similar_sentences;
"""

SELECT_TOTAL_NUMBER_OF_ARTICLES = """
select count(distinct article_id) from sentence;
"""

SELECT_TOTAL_NUMBER_OF_SENTENCES = """
select count(sentence) from sentence;
"""


def get_total_sentence_pairs_count(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_SENTENCE_PAIRS, (sentence_pair_score_threshold,))
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_unique_article_pairs_count(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_unique_article_pairs_with_common_named_entities(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_unique_article_pairs_with_more_than_2_sentences(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_MORE_THAN_2_SENTENCES, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_unique_article_pairs_without_common_named_entities_and_with_more_than_2_sentence(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITHOUT_COMMON_NAMED_ENTITIES_AND_WITH_MORE_THAN_2_SENTENCE, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_potential_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_EN_DE, (sentence_pair_score_threshold,))
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_potential_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_EN_PT, (sentence_pair_score_threshold,))
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_potential_similar_sentences_de_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_POTENTIAL_SIMILAR_SENTENCES_DE_PT, (sentence_pair_score_threshold,))
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_de_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_DE_PT, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_count_with_common_named_entities_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_negative_en_articles_with_common_named_entities_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_negative_en_articles_with_common_named_entities_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_with_common_named_entities_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_count_with_common_named_entities_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_with_common_named_entities_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_count_with_common_named_entities_de_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_DE_PT, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_article_pairs_with_common_named_entities_de_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLE_PAIRS_WITH_COMMON_NAMED_ENTITIES_DE_PT, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_more_than_2_sentences_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_more_than_2_sentences_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_more_than_2_sentences_de_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_MORE_THAN_2_SENTENCES_DE_PT, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_count_with_common_named_entities_and_multiple_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_negative_en_articles_with_common_named_entities_and_multiple_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_negative_en_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_count_with_common_named_entities_and_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_count_with_common_named_entities_and_multiple_similar_sentences_de_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_DE_PT, (sentence_pair_score_threshold,))
        return database_cursor.rowcount
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_common_named_entities_and_multiple_similar_sentences_de_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_AND_MULTIPLE_SIMILAR_SENTENCES_DE_PT, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_common_named_entities_or_multiple_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_OR_MULTIPLE_SIMILAR_SENTENCES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_unique_articles_with_common_named_entities_or_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_UNIQUE_ARTICLES_WITH_COMMON_NAMED_ENTITIES_OR_MULTIPLE_SIMILAR_SENTENCES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_negative_en_articles_with_common_named_entities_or_multiple_similar_sentences_en_de(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_OR_MULTIPLE_SIMILAR_SENTENCES_EN_DE, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_false_negative_en_articles_with_common_named_entities_or_multiple_similar_sentences_en_pt(sentence_pair_score_threshold, database_cursor):
    try:
        database_cursor.execute(SELECT_FALSE_NEGATIVE_EN_ARTICLES_WITH_COMMON_NAMED_ENTITIES_OR_MULTIPLE_SIMILAR_SENTENCES_EN_PT, (sentence_pair_score_threshold,))
        return database_cursor.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_number_of_articles(database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_NUMBER_OF_ARTICLES, ())
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_total_number_of_sentences(database_cursor):
    try:
        database_cursor.execute(SELECT_TOTAL_NUMBER_OF_SENTENCES, ())
        result = database_cursor.fetchone()
        return result[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)