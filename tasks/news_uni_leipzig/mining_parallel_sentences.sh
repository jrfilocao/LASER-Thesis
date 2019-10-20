#!/bin/bash

if [ -z ${LASER+x} ] ; then
  echo "Please set the environment variable 'LASER'"
  exit
fi

# general config
bucc_edition="bucc2018"
root_directory="."
bucc_tar_files_directory=${root_directory}/downloaded # tar files as distrubuted by the BUCC evaluation
bucc_raw_texts_directory=${root_directory}/${bucc_edition} # raw texts of BUCC
normalized_texts_embeddings_directory=${root_directory}/embed # normalized texts and embeddings
languages=("de" "pt")
target_language="en" # English is always the 2nd language

# encoder
models_directory="${LASER}/models"
encoder="${models_directory}/bilstm.93langs.2018-12-26.pt"
bpe_codes="${models_directory}/93langs.fcodes"


###################################################################
#
# Extract files with labels and texts from the BUCC corpus
#
###################################################################

split_entries_into_ids_and_sentences () {
  dataset_path=$1; dataset_type=$2; source_language=$3
  file_output="${normalized_texts_embeddings_directory}/${bucc_edition}.${source_language}-${target_language}.${dataset_type}"
  for language in ${target_language} ${source_language} ; do
    dataset_path_for_language="${bucc_raw_texts_directory}/${dataset_path}.${language}"
    if [ ! -f ${file_output}.txt.${language} ] ; then
      echo " - extract files ${file_output} in ${language}"
      cat ${dataset_path_for_language} | cut -f1 > ${file_output}.id.${language}
      cat ${dataset_path_for_language} | cut -f2 > ${file_output}.txt.${language}
    fi
  done
}


###################################################################
#
# Tokenize and Embed
#
###################################################################

Embed () {
  language=$2
  text_for_language="$1.txt.${language}"
  sentence_embedding_output_path_for_language="$1.enc.${language}"
  if [ ! -s ${sentence_embedding_output_path_for_language} ] ; then
    cat ${text_for_language} | python3 ${LASER}/source/embed.py \
      --encoder ${encoder} \
      --token-lang ${language} \
      --bpe-codes ${bpe_codes} \
      --output ${sentence_embedding_output_path_for_language} \
      --verbose
  fi
}


###################################################################
#
# Mine for bitexts
#
###################################################################

Mine () {
  dataset_path=$1
  first_language=$2
  second_language=$3
  candidates="${dataset_path}.candidates.tsv"
  if [ ! -s ${candidates} ] ; then
    python3 ${LASER}/source/mine_bitexts.py \
       ${dataset_path}.txt.${first_language} ${dataset_path}.txt.${second_language} \
       --src-lang ${first_language} --trg-lang ${second_language} \
       --src-embeddings ${dataset_path}.enc.${first_language} --trg-embeddings ${dataset_path}.enc.${second_language} \
       --unify --mode mine --retrieval max --margin ratio -k 4  \
       --output ${candidates} \
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

  split_entries_into_ids_and_sentences "${source_language}-${target_language}/${source_language}-${target_language}.sample" "dev" ${source_language}

  # Tokenize and embed train
  base_file_name="${bucc_edition}.${source_language}-${target_language}"
  dataset_path="${base_file_name}.train"
  Embed ${normalized_texts_embeddings_directory}/${dataset_path} ${source_language} ${encoder} ${bpe_codes}
  Embed ${normalized_texts_embeddings_directory}/${dataset_path} ${target_language} ${encoder} ${bpe_codes}

  # mine for texts in train
  Mine ${normalized_texts_embeddings_directory}/${dataset_path} ${source_language} ${target_language}

done

threshold=1.1
for source_language in ${languages[@]} ; do
  for target_language in ${languages[@]} ; do
    if [ ${source_language} != 'en' -a ${target_language} != "en" -a ${source_language} != ${target_language} ] ; then
      bitext="${bucc_edition}.${source_language}-${target_language}.train.extracted.th${threshold}.csv"
      if [ ! -s ${bitext} ] ; then
        echo "Extracting bitexts for ${source_language}-${target_language}"
        python3 ${LASER}/source/mine_bitexts.py \
          ${normalized_texts_embeddings_directory}/${bucc_edition}.${source_language}-en.train.txt.${source_language} \
          ${normalized_texts_embeddings_directory}/${bucc_edition}.${target_language}-en.train.txt.${target_language} \
          --src-lang ${source_language} --trg-lang ${target_language} \
          --src-embeddings ${normalized_texts_embeddings_directory}/${bucc_edition}.${source_language}-en.train.enc.${source_language} \
          --trg-embeddings ${normalized_texts_embeddings_directory}/${bucc_edition}.${target_language}-en.train.enc.${target_language} \
          --unify --mode mine --retrieval max --margin ratio -k 4  \
          --output ${bitext} --threshold ${threshold} \
          --verbose --gpu
      fi
    fi
  done
done
