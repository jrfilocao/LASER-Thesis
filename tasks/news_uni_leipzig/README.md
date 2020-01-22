# Finding similar cross-language news articles based on mining of parallel sentences

This project is divided into two parts:
* Mining of parallel sentences
* Finding similar news articles

## Mining of parallel sentences

* Run `./parallel_sentences_miner.sh `
    * Raw news article files in `./input_files` will be [processed](MINING_PARALLEL_SENTENCES.md)
    * Following output files will be created:
        * `de_id_sentence_pairs`
        * `en_id_sentence_pairs`
        * `pt_id_sentence_pairs`
        * `de_pt_sentence_candidates.tsv`
        * `en_de_sentence_candidates.tsv`
        * `en_pt_sentence_candidates.tsv`

#### Parsing results

* Total articles  =  **77850**
* English sentences = **1176047**
* German sentences = **170637**
* Portuguese sentences = **49451**

#### Mining results

* EN <-> DE = **106**
* EN <-> PT = **189**
* DE <-> PT = **11**

## Finding similar news articles

* Run `./id_sentence_pair_persister.py --id-sentence-pair-files de_id_sentence_pairs en_id_sentence_pairs pt_id_sentence_pairs`
    * Loads data into `sentence` table
* Run `./article_similarity_finder.py --sentence-candidate-file-paths output_files/de_pt_sentence_candidates.tsv --file-language-pairs de_pt`
    * [Similarity check](FINDING_SIMILAR_NEWS_ARTICLES.MD) will be done
    * Database tables **sentence** for id-sentence pairs and **matched_article** for articles similarity results will be created
 
#### Similarity results
 
* EN <-> DE
    * Similar articles = **70**
    * Total potential related articles = **106**
    * Percentage of similar articles = **66%**
* EN <-> PT
    * Similar articles = **181**
    * Total potential related articles = **189**
    * Percentage of similar articles = **95%**
* DE <-> PT
    * Similar articles = **7**
    * Total potential related  articles = **11**
    * Percentage of similar articles = **63%**

##### Types of article similarities

###### EN <-> DE 
* Exact translation of **whole text**
    * Source: **Press room**

```
SELECT source_sentence, target_sentence, source_article_text, target_article_text, 
named_entities_score, source_article_url, target_article_url
FROM matched_article 
WHERE source_sentence = 'We have long focused on helping our clients find concrete, sustainable solutions to their needs..'
AND target_sentence = 'Wir konzentrieren uns seit langem darauf, unseren Kunden zu helfen, konkrete und nachhaltige Lösungen für ihre Bedürfnisse zu finden.'; 
```

* Exact translation of **citation**, same topic
    * Source **DE**: **News Agency Deutsche Presse-Agentur GmbH (DPA)**
    * Source **EN**: **News Agency Reuters**
    * German article divided into two articles in the database due to erroneous parsing

```
SELECT source_sentence, target_sentence, source_article_text, target_article_text, 
named_entities_score, source_article_url, target_article_url
FROM matched_article 
WHERE source_sentence = 'We have always said that, if it is to have a long-term future, our sport must preserve its historic venues and Silverstone and Great Britain represent the cradle of this sport, said Formula One chairman Chase Carey..'
AND target_sentence = 'Wir haben immer gesagt, dass unser Sport, wenn er eine langfristige Zukunft haben soll, seine historischen Austragungsorte bewahren muss, sagte Formel-1-Boss Chase Carey.';
```

###### DE <-> PT

* Exact translation of **citation**, same topic

```
SELECT source_sentence, target_sentence, source_article_text, target_article_text, 
named_entities_score, source_article_url, target_article_url
FROM matched_article 
WHERE source_sentence = 'Aber bis zum heutigen Tag wissen wir weder, wer ihn kaufen möchte noch zu welchem Preis, sagte Leonardo.'
AND target_sentence = 'Mas, até o momento, não sabemos se alguém quer comprá-lo ou a que preço.';
```

* Similar sentences but **no common** named-entities

```
SELECT source_sentence, target_sentence, source_article_text, target_article_text, 
named_entities_score, source_article_url, target_article_url
FROM matched_article 
WHERE source_sentence = 'So ein schwieriges Jahr habe ich in meiner Karriere noch nicht erlebt – das waren so viele Verletzungen.'
AND target_sentence = '– Foi um momento muito difícil na minha carreira, pois eu nunca tinha me machucado de forma tão grave assim.'
```

* **No similar** sentences and **no common** named-entities

```
SELECT source_sentence, target_sentence, source_article_text, target_article_text, 
named_entities_score, source_article_url, target_article_url
FROM matched_article 
WHERE source_sentence = 'Wir werden uns nicht vermehren, weil wir wissen, dass die Welt nicht damit umgehen kann..'
AND target_sentence = '- Não vão recorrer porque sabem que não conseguiriam nada.'
```


## TODOs
* Continue evaluating results
* Prepare presentation
* Organize code
    * Python best practises
    * 2 scripts only