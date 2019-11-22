# README

## Build
* Rebuid docker image after download of dependencies (it takes long) or before cloning the github project:
    *  `docker build --tag=laser docker --build-arg CACHEBUST=$(date +%s)`

## Finding sentences

`./sentence_finder.py --input-file-name=input_files/wdt_2019-07-08_pt --line-count=5 --average-line-word-count=20 --language=pt`

`./sentence_finder.py --input-file-name=input_files/wdt_2019-07-08_de --line-count=5 --average-line-word-count=15 --language=de`

`./sentence_finder.py --input-file-name=input_files/wdt_2019-07-08_en --line-count=5 --average-line-word-count=15 --language=en`

## TODOs
* Complement `parallel_sentences_miner.sh` to process all three pairs combinations:
    * **en-de**
    * **en-pt**
    * **pt-de**
* Complement `parallel_sentences_miner.sh` to process all seven days:
    * from **2019-07-08** till **2019-07-14**
* Run the experiment
* For each pair of the parallel sentences
    * Get named entities from their respective articles with the help of **NLTK** or **SpaCy**
    * If one named entity matches, then both articles match
    * Optional: Use JRC-Names to be sure that named entities are not handling the same subject 
    
    
    
    
