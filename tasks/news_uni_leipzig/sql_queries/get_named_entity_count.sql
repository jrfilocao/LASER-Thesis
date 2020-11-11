with and_entries as
(
select named_entities_score, source_article_id, target_article_id
from matched_article
where source_language = %s and target_language = %s
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.125
group by named_entities_score, matched_article.source_article_id, matched_article.target_article_id
),
brace_counts as
(
select CHAR_LENGTH(named_entities_score) - CHAR_LENGTH(REPLACE(named_entities_score, ',', '')) as ne_count,
source_article_id, target_article_id
from and_entries
)
select * from brace_counts where ne_count < 2;
