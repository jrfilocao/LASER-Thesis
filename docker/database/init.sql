CREATE TABLE sentence (
   sentence_id VARCHAR (200) PRIMARY KEY,
   article_id VARCHAR (200) NOT NULL,
   sentence VARCHAR (5000) NOT NULL
);

CREATE TABLE matched_article (
   source_article_id VARCHAR (200) NOT NULL,
   target_article_id VARCHAR (200) NOT NULL,
   source_sentence VARCHAR (5000) NOT NULL,
   target_sentence VARCHAR (5000) NOT NULL,
   source_article_text TEXT NOT NULL,
   target_article_text TEXT NOT NULL,
   named_entities_score TEXT
);