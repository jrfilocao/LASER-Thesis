#!/bin/bash

if [ -z ${LASER+x} ] ; then
  echo "Please set the environment variable 'LASER'"
  exit
fi

if [ -z ${NEWS_TASK+x} ] ; then
  echo "Please set the environment variable 'NEWS_TASK'"
  exit
fi

# general config
root_directory="."

# encoder
models_directory="${LASER}/models"
encoder="${models_directory}/bilstm.93langs.2018-12-26.pt"
bpe_codes="${models_directory}/93langs.fcodes"

extract_sentences () {
  input_file_name="${input_directory}/${input_base_file_name}_${language}"

  echo "input_file_name ${input_file_name} language ${language}"

  python3 ${NEWS_TASK}/extraction/news_article_extractor.py \
    --input-file-name ${input_file_name} \
    --line-count 5 \
    --average-line-word-count 20 \
    --language ${language}
}

embed_sentences () {
  sentences_file_path="${output_directory}/${language}_sentences"
  sentence_embedding_output_file_name="${output_directory}/${language}_embedding"

  if [ ! -s ${sentence_embedding_output_file_name} ] ; then
    cat ${sentences_file_path} | python3 ${LASER}/source/embed.py \
      --encoder ${encoder} \
      --token-lang ${language} \
      --bpe-codes ${bpe_codes} \
      --output ${sentence_embedding_output_file_name} \
      --verbose
  fi
}

mine_for_bitexts () {
  threshold=0.8
  sentence_candidates="${output_directory}/${source_language}_${target_language}_sentence_candidates.tsv"
  if [ ! -s ${sentence_candidates} ] ; then
    python3 ${LASER}/source/mine_bitexts.py \
       ${output_directory}/${source_language}_sentences ${output_directory}/${target_language}_sentences \
       --src-lang ${source_language} --trg-lang ${target_language} \
       --src-embeddings ${output_directory}/${source_language}_embedding --trg-embeddings ${output_directory}/${target_language}_embedding \
       --unify --mode mine --retrieval max --margin ratio -k 4  \
       --output ${sentence_candidates} --threshold ${threshold} \
       --verbose
  fi
}

persist_extracted_sentences () {
  python3 ${NEWS_TASK}/extraction/id_sentence_pair_persister.py \
    --id-sentence-pair-files \
      ${output_directory}/pt_id_sentence_pairs \
      ${output_directory}/de_id_sentence_pairs \
      ${output_directory}/en_id_sentence_pairs
}

find_and_persist_similar_articles () {
  python3 ${NEWS_TASK}/similarity/article_similarity_finder.py \
    --sentence-candidate-file-paths \
      ${output_directory}/de_pt_sentence_candidates.tsv \
      ${output_directory}/en_de_sentence_candidates.tsv \
      ${output_directory}/en_pt_sentence_candidates.tsv \
    --file-language-pairs de_pt en_de en_pt
}

find_and_write_triple_similar_articles () {
  python3 ${NEWS_TASK}/similarity/triple_similarity_finder.py
}

create_reports () {
  python3 ${NEWS_TASK}/reporting/statistics_report_creator.py --output-report-base-file-name ${output_directory}/report
}


###################################################################
#
# Main loop
#
###################################################################

echo -e "\nProcessing news articles"

input_directory="${NEWS_TASK}/input_files"
output_directory="${NEWS_TASK}/output_files"

input_base_file_names=(wdt_2019-07-08 wdt_2019-07-09 wdt_2019-07-10 wdt_2019-07-11 wdt_2019-07-12 wdt_2019-07-13 wdt_2019-07-14)
languages=(en pt de)

for input_base_file_name in "${input_base_file_names[@]}"; do
  for language in "${languages[@]}"; do
    echo -e "\nextract_sentences ${language}"
    extract_sentences
  done
done

echo -e "\npersist extracted sentences"
persist_extracted_sentences

for language in "${languages[@]}"; do
  echo -e "\nembed sentences ${language}"
  embed_sentences
done

language_pairs=( "en de" "en pt" "de pt")

for language_pair in "${language_pairs[@]}"; do
  IFS=' ' read -r -a language_pair_array <<< "$language_pair"
  source_language="${language_pair_array[0]}"
  target_language="${language_pair_array[1]}"
  echo -e "\nembed sentences ${source_language} ${target_language}"
  mine_for_bitexts
done

echo -e "\nfind and persist similar articles"
find_and_persist_similar_articles

echo -e "\nfind and write triple similar articles"
find_and_write_triple_similar_articles

echo -e "\ncreate reports"
create_reports