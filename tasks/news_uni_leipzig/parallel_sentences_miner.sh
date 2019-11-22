#!/bin/bash

if [ -z ${LASER+x} ] ; then
  echo "Please set the environment variable 'LASER'"
  exit
fi

# general config
root_directory="."

# encoder
models_directory="${LASER}/models"
encoder="${models_directory}/bilstm.93langs.2018-12-26.pt"
bpe_codes="${models_directory}/93langs.fcodes"


embed_sentences () {
  sentence_base_file_name=$1
  language=$2

  sentence_file_name="${sentence_base_file_name}_${language}_sentences"
  sentence_embedding_output_file_name="${language}_embedding"

  if [ ! -s ${sentence_embedding_output_file_name} ] ; then
    cat ${sentence_file_name} | python3 ${LASER}/source/embed.py \
      --encoder ${encoder} \
      --token-lang ${language} \
      --bpe-codes ${bpe_codes} \
      --output ${sentence_embedding_output_file_name} \
      --verbose
  fi
}

mine_for_bitexts () {
  sentence_base_file_name=$1
  source_language=$2
  target_language=$3
  threshold=1.1
  sentence_candidates="${base_file_name}_${source_language}_${target_language}_sentence_candidates.tsv"
  if [ ! -s ${sentence_candidates} ] ; then
    python3 ${LASER}/source/mine_bitexts.py \
       ${sentence_base_file_name}_${source_language}_sentences ${sentence_base_file_name}_${target_language}_sentences \
       --src-lang ${source_language} --trg-lang ${target_language} \
       --src-embeddings ${sentence_base_file_name}_${source_language}_embedding --trg-embeddings ${sentence_base_file_name}_${target_language}_embedding \
       --unify --mode mine --retrieval max --margin ratio -k 4  \
       --output ${sentence_candidates} --threshold ${threshold} \
       --verbose
  fi
}


###################################################################
#
# Main loop
#
###################################################################

echo -e "\nProcessing id/sentence-pair from news articles"

languages=(en pt de)

for language in "${languages[@]}"; do
  embed_sentences ${root_directory}/ ${language}
done

language_pairs=( 'en de' 'en pt' 'de pt')

for language_pair in "${language_pairs[@]}"; do
  IFS=' ' read -r -a language_pair_array <<< "$language_pair"
  source_language="${language_pair_array[0]}"
  target_language="${language_pair_array[1]}"

  mine_for_bitexts ${root_directory}/ ${source_language} ${target_language}

done