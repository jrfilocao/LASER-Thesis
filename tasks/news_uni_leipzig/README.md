# README

## Build
* Rebuid docker image after download of dependencies (it takes long) or before cloning the github project:
    *  `docker build --tag=laser docker --build-arg CACHEBUST=$(date +%s)`

## Finding sentences

`./sentence_finder.py --input-file-name=input_files/wdt_2019-07-08_pt --line-count=5 --average-line-word-count=20 --language=pt`

`./sentence_finder.py --input-file-name=input_files/wdt_2019-07-08_de --line-count=5 --average-line-word-count=15 --language=de`

`./sentence_finder.py --input-file-name=input_files/wdt_2019-07-08_en --line-count=5 --average-line-word-count=15 --language=en`

## Input file informations

* input_files/wdt_2019-07-08_en
    * Number of articles = **9505**
    * Number of valid sentences = **187666**

* input_files/wdt_2019-07-08_pt
    * Number of articles = **567**
    * Number of valid sentences = **7602**

* input_files/wdt_2019-07-08_de
    * Number of articles = **1475**
    * Number of valid sentences = **25274**

* input_files/wdt_2019-07-09_en
    * Number of articles = **10105**
    * Number of valid sentences = **190533**

* input_files/wdt_2019-07-09_pt
    * Number of articles = **573**
    * Number of valid sentences = **7149**

* input_files/wdt_2019-07-09_de
    * Number of articles = **1468**
    * Number of valid sentences = **25098**

* input_files/wdt_2019-07-10_en
    * Number of articles = **10855**
    * Number of valid sentences = **188634**

* input_files/wdt_2019-07-10_pt
    * Number of articles = **596**
    * Number of valid sentences = **7873**

* input_files/wdt_2019-07-10_de
    * Number of articles = **1781**
    * Number of valid sentences = **30233**

* input_files/wdt_2019-07-11_en
    * Number of articles = **10819**
    * Number of valid sentences = **196681**

* input_files/wdt_2019-07-11_pt
    * Number of articles = **593**
    * Number of valid sentences = **7353**

* input_files/wdt_2019-07-11_de
    * Number of articles = **1602**
    * Number of valid sentences = **28231**

* input_files/wdt_2019-07-12_en
    * Number of articles = **10793**
    * Number of valid sentences = **205116**

* input_files/wdt_2019-07-12_pt
    * Number of articles = **658**
    * Number of valid sentences = **8509**

* input_files/wdt_2019-07-12_de
    * Number of articles = **1413**
    * Number of valid sentences = **24630**

* input_files/wdt_2019-07-13_en
    * Number of articles = **6315**
    * Number of valid sentences = **106792**

* input_files/wdt_2019-07-13_pt
    * Number of articles = **485**
    * Number of valid sentences = **6331**

* input_files/wdt_2019-07-13_de
    * Number of articles = **969**
    * Number of valid sentences = **18304**

* input_files/wdt_2019-07-14_en
    * Number of articles = **5795**
    * Number of valid sentences = **99559**

* input_files/wdt_2019-07-14_pt
    * Number of articles = **351**
    * Number of valid sentences = **4584**

* input_files/wdt_2019-07-14_de
    * Number of articles = **1132**
    * Number of valid sentences = **18685**

Total articles =  **77850**

#### Number of sentences

* german sentences = **170637**
* portuguese sentences = **49451**
* english sentences = **1176047** 

## TODOs
* Complement `parallel_sentences_miner.sh` to process all three pairs combinations: **OK**
    * **en-de**
    * **en-pt**
    * **pt-de**
* Complement `parallel_sentences_miner.sh` to process all seven days: **OK**
    * from **2019-07-08** till **2019-07-14**
* These combinations of date and language should have only one output such as: **OK**
    * **english_sentences**
    * **german_sentences**
    * **portuguese_sentences**

* Run the experiment
* For each pair of the parallel sentences
    * Get named entities from their respective articles with the help of **NLTK** or **SpaCy**
    * If one named entity matches, then both articles match
    * Optional: Use JRC-Names to be sure that named entities are not handling the same subject 
