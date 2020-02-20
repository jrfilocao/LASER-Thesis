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