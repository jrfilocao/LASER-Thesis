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

###### 1.1 Laser threshold, July 2019, 10 minimum words per sentence in extraction phase

* Total sentence pairs: **306**
* Unique article pairs: **212**
* Unique articles with more than 2 sentences: **37**
* Article without common named-entities and with more than 2 sentences: **1** 
* EN <-> DE
    * Total potential similar sentences = **106**
    * Unique articles = **85**
    * Unique articles with named-entities = **51** 
    * Percentage of similar articles = **60%**
    * Articles with multiple similar sentences = **7**
* EN <-> PT
    * Total potential similar sentences = **181**
    * Unique articles = **115**
    * Unique articles with named-entities = **108**
    * Percentage of similar articles = **94%**
    * Articles with multiple similar sentences = **30**
* DE <-> PT
    * Total potential similar sentences = **11**
    * Unique articles = **11**
    * Unique articles with named-entities = **7**
    * Percentage of similar articles = **63%**
    * Articles with multiple similar sentences = **0**

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

* More than one sentence-pair similar, no similar named-entities: * **Einziger Fall** * bei 1.1 Laser threshold
    * Named-entities: EN: **Ferraris**, DE: **Ex-Ferrari-Teamchef**
        * Also due to partial texts because of bad text extraction
    * Translations of **    citations**

```
SELECT source_sentence, target_sentence, source_article_text, target_article_text, 
named_entities_score, source_article_url, target_article_url
FROM matched_article
WHERE
source_article_id = 'input_files/wdt_2019-07-12_en_article_1587'
AND
target_article_id = 'input_files/wdt_2019-07-12_de_article_210';
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

###### EN <-> PT

* Article translation from **Reuters**. **Multiple** sentences. **Multiple** named-entities.
    * Article URL EN: https://www.reuters.com/article/us-china-xinjiang-rights/saudi-arabia-and-russia-among-37-states-backing-chinas-xinjiang-policy-idUSKCN1U721X
    * Article URL PT: https://oglobo.globo.com/mundo/arabia-saudita-russia-mais-35-paises-apoiam-politicas-da-china-para-muculmanos-uigures-23803783
    

```
SELECT source_sentence, target_sentence, source_article_text, target_article_text, 
named_entities_score, source_article_url, target_article_url
FROM matched_article
WHERE
source_article_id = 'input_files/wdt_2019-07-14_en_article_4297'
AND
target_article_id = 'input_files/wdt_2019-07-12_pt_article_89';
```


## TODOs
* Continue evaluating results
* Prepare presentation
* Organize code
    * Python best practises
    * 2 scripts only