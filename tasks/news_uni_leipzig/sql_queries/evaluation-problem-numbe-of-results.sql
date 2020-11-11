select source_article_id, target_article_id                                                                 from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.125
and substring(source_article_id, 0, 58) != substring(target_article_id, 0, 58)
group by matched_article.source_article_id, matched_article.target_article_id;

with count_unique_en_de as
(
select source_article_id, target_article_id, count(*) as number_of_common_phrases
from matched_article
where source_language = 'en' and target_language = 'de'
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from count_unique_en_de
inner join matched_article
on count_unique_en_de.source_article_id = matched_article.source_article_id
and count_unique_en_de.target_article_id = matched_article.target_article_id
where number_of_common_phrases  != number_of_similar_sentences; -- 6892


with count_unique_en_de as
(
select source_article_id, target_article_id, count(*) as number_of_common_phrases
from matched_article
where source_language = 'en' and target_language = 'de'
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from count_unique_en_de; -- 690993

and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.125
and substring(source_article_id, 0, 58) != substring(target_article_id, 0, 58)



select source_sentence, target_sentence, sentence_candidates_score,number_of_similar_sentences
from matched_article
where source_article_id like '%2020-01-21_en_article_12421'
and target_article_id like '%2019-07-08_de_article_367';
