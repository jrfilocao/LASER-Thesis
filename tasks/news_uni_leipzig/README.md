# README

This project is divided into two parts:
* Mining of parallel sentences
* Finding similar news articles

### Mining of parallel sentences

* Run --sentence-files README.md file_writer.py`./parallel_sentences_miner.sh `
    * Raw news article files in `./input_files` will be [processed](MINING_PARALLEL_SENTENCES.md)
    * Following output files will be created:
        * `de_id_sentence_pairs`
        * `en_id_sentence_pairs`
        * `pt_id_sentence_pairs`
        * `de_pt_sentence_candidates.tsv`
        * `en_de_sentence_candidates.tsv`
        * `en_pt_sentence_candidates.tsv`

##### Parsing results

* Total articles  =  **77850**
* English sentences = **1176047**
* German sentences = **170637**
* Portuguese sentences = **49451**

##### Mining results

* EN <-> DE = **106**
* EN <-> PT = **189**
* DE <-> PT = **11**

### Finding similar news articles

* Run `./id_sentence_pair_persister.py --id-sentence-pair-files de_id_sentence_pairs en_id_sentence_pairs pt_id_sentence_pairs`
    * Loads data into `sentence` table
* Run `./article_similarity_finder.py --sentence-candidate-file-paths output_files/de_pt_sentence_candidates.tsv --file-language-pairs de_pt`
    * Gets articles from **sentence candidates**
    * Compares articles named-entities
    * Saves articles similarity results into table `matched_articles`
 
 ##### Similarity results
 
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