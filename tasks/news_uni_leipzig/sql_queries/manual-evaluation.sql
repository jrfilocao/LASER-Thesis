-- UNIQUE
-- EN DE
with unique_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from unique_sql;

-- EN PT
with unique_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from unique_sql;

-- DE PT
with unique_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from unique_sql;

-- AND
-- EN DE
with and_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from and_sql;

-- EN PT
with and_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from and_sql;

-- DE PT
with and_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and named_entities_score is not null
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from and_sql;


-- OR
-- EN DE
with or_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from or_sql;

-- EN PT
with or_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from or_sql;

-- DE PT
with or_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and number_of_similar_sentences > 1
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from or_sql;

-- ONLY
-- EN DE
with only_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'de'
and named_entities_score is not null
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from only_sql;

-- EN PT
with only_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'en' and target_language = 'pt'
and named_entities_score is not null
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from only_sql;

-- DE PT
with only_sql as
(
select source_article_id, target_article_id
from matched_article
where source_language = 'de' and target_language = 'pt'
and named_entities_score is not null
and sentence_candidates_score >= 1.05
group by matched_article.source_article_id, matched_article.target_article_id
)
select count(*) from only_sql;
