CREATE TABLE sentence (
   id SERIAL PRIMARY KEY,
   sentence_id VARCHAR (200) NOT NULL,
   article_id VARCHAR (200) NOT NULL,
   sentence VARCHAR (5000) NOT NULL
);

CREATE TABLE matched_article (
   id SERIAL PRIMARY KEY,
   source_article_id VARCHAR (200) NOT NULL,
   target_article_id VARCHAR (200) NOT NULL,
   source_sentence VARCHAR (5000) NOT NULL,
   target_sentence VARCHAR (5000) NOT NULL,
   source_article_text TEXT NOT NULL,
   target_article_text TEXT NOT NULL,
   source_language VARCHAR (2) NOT NULL,
   target_language VARCHAR (2) NOT NULL,
   named_entities_score TEXT,
   sentence_candidates_score FLOAT,
   number_of_similar_sentences INT
);