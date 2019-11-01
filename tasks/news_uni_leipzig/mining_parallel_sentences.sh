#!/bin/bash

if [ -z ${LASER+x} ] ; then
  echo "Please set the environment variable 'LASER'"
  exit
fi

# general config
root_directory="."
languages=("de")
target_language="en" # English is always the 2nd language

# encoder
models_directory="${LASER}/models"
encoder="${models_directory}/bilstm.93langs.2018-12-26.pt"
bpe_codes="${models_directory}/93langs.fcodes"


embed_sentences () {
  sentence_base_file_name=$1
  language=$2

  sentence_file_name="${sentence_base_file_name}_${language}_sentences"
  sentence_embedding_output_file_name="${sentence_base_file_name}_${language}_embedding"

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
  sentence_candidates="${base_file_name}_${source_language}_${target_language}_sentence_candidates.tsv"
  if [ ! -s ${sentence_candidates} ] ; then
    python3 ${LASER}/source/mine_bitexts.py \
       ${sentence_base_file_name}_${source_language}_sentences ${sentence_base_file_name}_${target_language}_sentences \
       --src-lang ${source_language} --trg-lang ${target_language} \
       --src-embeddings ${sentence_base_file_name}_${source_language}_embedding --trg-embeddings ${sentence_base_file_name}_${target_language}_embedding \
       --unify --mode mine --retrieval max --margin ratio -k 4  \
       --output ${sentence_candidates} \
       --verbose --gpu
  fi
}


###################################################################
#
# Main loop
#
###################################################################

echo -e "\nProcessing id/sentence-pair from news articles"

for source_language in ${languages[@]} ; do

  base_file_name="wdt_2019-07-08" # TODO remove later
  embed_sentences ${root_directory}/${base_file_name} ${source_language}
  embed_sentences ${root_directory}/${base_file_name} ${target_language}

  mine_for_bitexts ${root_directory}/${base_file_name} ${source_language} ${target_language}

done
#
#threshold=1.1
#for source_language in ${languages[@]} ; do
#  for target_language in ${languages[@]} ; do
#    if [ ${source_language} != 'en' -a ${target_language} != "en" -a ${source_language} != ${target_language} ] ; then
#      bitext="${bucc_edition}.${source_language}-${target_language}.train.extracted.th${threshold}.csv"
#      if [ ! -s ${bitext} ] ; then
#        echo "Extracting bitexts for ${source_language}-${target_language}"
#        python3 ${LASER}/source/mine_bitexts.py \
#          ${normalized_texts_embeddings_directory}/${bucc_edition}.${source_language}-en.train.txt.${source_language} \
#          ${normalized_texts_embeddings_directory}/${bucc_edition}.${target_langu  age}-en.train.txt.${target_language} \
#          --src-lang ${source_language} --trg-lang ${target_language} \
#          --src-embeddings ${normalized_texts_embeddings_directory}/${bucc_edition}.${source_language}-en.train.enc.${source_language} \
#          --trg-embeddings ${normalized_texts_embeddings_directory}/${bucc_edition}.${target_language}-en.train.enc.${target_language} \
#          --unify --mode mine --retrieval max --margin ratio -k 4  \
#          --output ${bitext} --threshold ${threshold} \
#          --verbose --gpu
#      fi
#    fi
#  done
#done
